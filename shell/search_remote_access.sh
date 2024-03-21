echo ''
echo '... ENTER'
echo ''
echo 'search access.log for IPs other than "170.250.88.62" ... START'
echo '  running...'
echo '  $ less +G access.log | grep -wv 170.250.88.62 | grep avm'
echo ''
echo ''
less +G access.log | grep -wv 170.250.88.62 | grep avm
echo ''
echo ''
echo 'search access.log for IPs other than "170.250.88.62" ... DONE'
echo '  just ran...'
echo '  $ less +G access.log | grep -wv 170.250.88.62 | grep avm'
echo ''
echo 'other printing examples...'
echo '  $ less +G access.log | grep -e 30/Jul/2022 -e 29/Jul/2022 | grep avm | grep -wv 170.250.88.62'
echo '  $ less +G dev.log | grep -w 2022-07-29 | grep -w 17:57 '
echo ''
echo '... EXIT'
echo ''


#less +G dev.log | grep -w 2022-07-29 | grep -w 17:57
#less +G access.log | grep -e 30/Jul/2022 -e 29/Jul/2022 | grep avm | grep -wv 170.250.88.62
