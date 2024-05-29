// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// remote compile
// import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
// import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
// import "@openzeppelin/contracts/access/Ownable.sol";
// import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
// import "@openzeppelin/contracts/utils/math/SafeMath.sol";

// local compile
import "../node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../node_modules/@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "../node_modules/@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "../node_modules/@openzeppelin/contracts/math/SafeMath.sol";

contract StakingContract is Ownable, ReentrancyGuard {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    struct UserInfo {
        uint256 amount;
        uint256 rewardDebt; // reward tokens owed to user
    }

    struct PoolInfo {
        IERC20 stakingToken;
        uint256 allocPoint; // amount of reward token allocation per pool, measured in points
        uint256 lastRewardBlock; // block number last time reewards were distributed
        uint256 accRewardPerShare; // accumulated reward per share
    }

    IERC20 public rewardToken;
    uint256 public rewardTokenPerBlock;
    PoolInfo[] public poolInfo;
    mapping(uint256 => mapping(address => UserInfo)) public userInfo;
    uint256 public totalAllocPoint; // total amount of allocation points
    uint256 public startBlock;

    event Deposit(address indexed user, uint256 indexed pid, uint256 amount);
    event Withdraw(address indexed user, uint256 indexed pid, uint256 amount);
    event EmergencyWithdraw(
        address indexed user,
        uint256 indexed pid,
        uint256 amount
    );

    constructor(
        IERC20 _rewardToken,
        uint256 _rewardTokenPerBlock,
        uint256 _startBlock
    ) Ownable(msg.sender) {
        rewardToken = _rewardToken;
        rewardTokenPerBlock = _rewardTokenPerBlock;
        startBlock = _startBlock;

        // Add a default pool for the rewardToken (pid: 0)
        poolInfo.push(
            PoolInfo({
                stakingToken: _rewardToken,
                allocPoint: 1000, // allocation of initial pool
                lastRewardBlock: startBlock,
                accRewardPerShare: 0
            })
        );
        totalAllocPoint = 1000; // initial total allocation across all pools; increases as new pools are added 
    }

    //  ensure that the provided pool identifier (_pid) is valid
    modifier validatePool(uint256 _pid) {
        require(_pid < poolInfo.length, "Pool ID invalid");
        _;
    }

    // HOUSE_052724: add missing function to get length of poolInfo array
    function poolLength() external view returns(uint256) {
        return poolInfo.length;
    }

    // Function to retrieve the amount of reward tokens held by the contract
    function getRewardTokenBalance() external view returns (uint256) {
        return rewardToken.balanceOf(address(this));
    }

    function setRewardPerBlock(uint256 _rewardTokenPerBlock) external onlyOwner {
        rewardTokenPerBlock = _rewardTokenPerBlock;
    }

    // allows the contract owner to add a new staking pool
    function addPool(IERC20 _stakingToken, uint256 _allocPoint) external onlyOwner {
        require(address(_stakingToken) != address(0), "Invalid staking token");
        require(_allocPoint > 0, "Allocation point must be greater than 0");

        uint256 lastRewardBlock = block.number > startBlock ? block.number : startBlock;
        poolInfo.push(
            PoolInfo({
                stakingToken: _stakingToken,
                allocPoint: _allocPoint,
                lastRewardBlock: lastRewardBlock,
                accRewardPerShare: 0
            })
        );
        totalAllocPoint = totalAllocPoint.add(_allocPoint);
    }

    // internal function that updates the reward information for a specific staking pool
    function updatePool(uint256 _pid) internal validatePool(_pid) {
        PoolInfo storage pool = poolInfo[_pid];
        if (block.number <= pool.lastRewardBlock) {
            return;
        }

        uint256 lpSupply = pool.stakingToken.balanceOf(address(this));
        if (lpSupply == 0) {
            pool.lastRewardBlock = block.number;
            return;
        }

        uint256 blocksSinceLastReward = block.number.sub(pool.lastRewardBlock);
        uint256 reward = blocksSinceLastReward.mul(rewardTokenPerBlock).mul(pool.allocPoint).div(totalAllocPoint);

        rewardToken.safeTransfer(dev(), reward.div(10));
        rewardToken.safeTransfer(address(this), reward);

        pool.accRewardPerShare = pool.accRewardPerShare.add(reward.mul(1e12).div(lpSupply));
        pool.lastRewardBlock = block.number;
    }

    function pendingReward(uint256 _pid, address _user) external view validatePool(_pid) returns (uint256) {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][_user];
        uint256 accRewardPerShare = pool.accRewardPerShare;
        uint256 lpSupply = pool.stakingToken.balanceOf(address(this));

        if (block.number > pool.lastRewardBlock && lpSupply != 0) {
            uint256 blocksSinceLastReward = block.number.sub(pool.lastRewardBlock);
            uint256 reward = blocksSinceLastReward.mul(rewardTokenPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
            accRewardPerShare = accRewardPerShare.add(reward.mul(1e12).div(lpSupply));
        }

        return user.amount.mul(accRewardPerShare).div(1e12).sub(user.rewardDebt);
    }

    function massUpdatePools() external {
        uint256 length = poolInfo.length;
        for (uint256 pid = 0; pid < length; ++pid) {
            updatePool(pid);
        }
    }

    //  allows the owner to update the allocation points for a specific pool
    function updateblocksSinceLastReward(uint256 _pid, uint256 _allocPoint) external onlyOwner {
        PoolInfo storage pool = poolInfo[_pid];
        uint256 prevAllocPoint = pool.allocPoint;
        pool.allocPoint = _allocPoint;

        if (prevAllocPoint != _allocPoint) {
            totalAllocPoint = totalAllocPoint.sub(prevAllocPoint).add(_allocPoint);
            updateStakingPool();
        }

        updatePool(_pid);
    }

    // updates the allocation points of a default staking pool (pid: 0) based on the allocation points of other pools
    function updateStakingPool() internal {
        uint256 length = poolInfo.length;
        uint256 points = 0;

        for (uint256 pid = 1; pid < length; ++pid) {
            points = points.add(poolInfo[pid].allocPoint);
        }

        if (points != 0) {
            points = points.div(3);
            totalAllocPoint = totalAllocPoint.sub(poolInfo[0].allocPoint).add(points);
            poolInfo[0].allocPoint = points;
        }
    }

    // allows a user to deposit tokens into a specific pool for staking
    // function deposit(uint256 _pid, uint256 _amount) external validatePool(_pid) nonReentrant {
    function deposit(uint256 _pid, uint256 _amount) external validatePool(_pid) {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        updatePool(_pid);

        if (user.amount > 0) {
            uint256 pending = user.amount.mul(pool.accRewardPerShare).div(1e12).sub(user.rewardDebt);
            safeRewardTransfer(msg.sender, pending);
        }

        if (_amount > 0) {
            pool.stakingToken.safeTransferFrom(address(msg.sender), address(this), _amount);
            user.amount = user.amount.add(_amount);
        }

        user.rewardDebt = user.amount.mul(pool.accRewardPerShare).div(1e12);
        emit Deposit(msg.sender, _pid, _amount);
    }

    // allows a user to withdraw their staked tokens from a specific pool
    // function withdraw(uint256 _pid, uint256 _amount) external validatePool(_pid) nonReentrant {
    function withdraw(uint256 _pid, uint256 _amount) external validatePool(_pid) {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(user.amount >= _amount, "Withdraw: not good");
        updatePool(_pid);

        uint256 pending = user.amount.mul(pool.accRewardPerShare).div(1e12).sub(user.rewardDebt);
        if (pending > 0) {
            safeRewardTransfer(msg.sender, pending);
        }

        if (_amount > 0) {
            user.amount = user.amount.sub(_amount);
            pool.stakingToken.safeTransfer(address(msg.sender), _amount);
        }

        user.rewardDebt = user.amount.mul(pool.accRewardPerShare).div(1e12);
        emit Withdraw(msg.sender, _pid, _amount);
    }

    // withdraw initial deposit back to your wallet in event of hack or bug, at the cost of losing reward balance
    // function emergencyWithdraw(uint256 _pid) external validatePool(_pid) nonReentrant {
    function emergencyWithdraw(uint256 _pid) external validatePool(_pid) {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        pool.stakingToken.safeTransfer(address(msg.sender), user.amount);
        emit EmergencyWithdraw(msg.sender, _pid, user.amount);
        user.amount = 0;
        user.rewardDebt = 0;
    }

    // transfer reward tokens to stakers
    function safeRewardTransfer(address _to, uint256 _amount) internal {
        uint256 rewardBalance = rewardToken.balanceOf(address(this));
        if (_amount > rewardBalance) {
            rewardToken.safeTransfer(_to, rewardBalance);
        } else {
            rewardToken.safeTransfer(_to, _amount);
        }
    }

    // function to allow anyone to deposit reward tokens
    function depositRewardTokens(uint256 _amount) external {
        rewardToken.safeTransferFrom(msg.sender, address(this), _amount);
    }

    function dev() internal view returns (address) {
        return owner();
    }
}
