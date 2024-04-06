__fname = 'bearshares'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

import logging
import json
from flask import Flask
from flask import request,redirect,Response
# import sites_env #required: sites_envs/__init__.py
from _env import env
from req_handler import *

GLOBAL_PATH_DEV_LOGS = env.GLOBAL_PATH_DEV_LOGS
GLOBAL_PATH_ISE_LOGS = env.GLOBAL_PATH_ISE_LOGS

print(__filename, f"\n IMPORTs complete:- STARTING -> file '{__filename}' . . . ")

logging.basicConfig(filename=GLOBAL_PATH_DEV_LOGS, level=logging.DEBUG)
logging.info(f'*======================================================================*')
logging.info(f'*                 server started -> {__filename} called                *')
logging.info(f'*======================================================================*')

app = Flask(__name__)

if __name__ == '__main__':
    app.run() #app.run(debug=True)

if not app.debug:
    from logging import FileHandler
    file_handler = FileHandler(GLOBAL_PATH_ISE_LOGS)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

#=====================================================#
### testing endpoints ###
#=====================================================#
@app.route('/bearshares')
def slash():
    return f"Why would you go with just '/bearshares'? Are you trying access the root? --> :P {__fname}"

@app.route('/bearshares/api', methods=['GET', 'POST'])
def slash_api():
    return f"/bearshares/api successful! {__fname}"

@app.route('/bearshares/api/request', methods=['GET', 'POST'])
def slash_request():
    return f"/bearshares/api/request successful! {__fname}"

@app.route('/bearshares/api/request/test', methods=['GET', 'POST'])
def slash_request_test():
    return f"/bearshares/api/request/test successful! {__fname}"


#=====================================================#
## NOTES ##
# ref: https://www.quora.com/What-is-the-technology-stack-behind-Uber?redirected_qid=572124
#   (psql plugin good for map integration: Postgis)
#
# Http Requests
#   Default:
#       content-type : application/x-www-form-urlencoded
#       (example: m_phone=1234567890&f_name=helloworld)
#
#   TODO: research setting json content-type
#       content-type : application/json
#       (example: easyHttp & wireshark testing needed)
#=====================================================#`

#=====================================================#
#         BST mobile Client Endpoints      #
#=====================================================#
kUserId = "user_id"

#==========================================#
## BST request paths & methods ##
#==========================================#
strUriHit = ' :-- URI hit --: '
strUrnHit = ' :-- URN hit --: '
strUrlHit = ' :-- URL hit --: '
strIPAddr = ' :-- IP Addr --: '
strMethod = ' :-- Methods --: '

strPrefix_v1 = '/bearshares/api/v1'


#===== SETTINGS (default - inactive) =====#
kPathGetInitSett = strPrefix_v1 + '/getinit/settings' # get initial settings
lst_MethGetInitSett = ['POST']

#===== trinity =====#
# POST execute TG cmd: /trinity_submit_shill
#   request params key_vals={tg_cmd_sim, tg_user_at, tweet_url}
kPathPOST_SubmitShill = strPrefix_v1 + '/bst/submit_shill_web'
lstMeth_SubmitShill = ['POST']

# POST execute TG cmd: /trinity_request_cashout
#   request params key_vals={tg_cmd_sim, tg_user_at}
kPathPOST_RequestPay = strPrefix_v1 + '/bst/request_pay_web'
lstMeth_RequestPay = ['POST']

# POST execute TG cmds: /trinit_show_my_rates /trinit_show_my_earnings /admin_show_user_shills
#   request params key_vals={tg_cmd_sim, tg_user_at}
kPathPOST_GetShillerInfo = strPrefix_v1 + '/bst/shiller_info_web'
lstMeth_GetShillerInfo = ['POST']

#============================================================================================================#
## Trinity TG bot data request APIs
#============================================================================================================#
@app.route(kPathPOST_SubmitShill, methods=lstMeth_SubmitShill)
def SubmitShill():
    printRequestMeta(request, kPathPOST_SubmitShill, lstMeth_SubmitShill, request.remote_addr)
    return bst_web_request(request)

@app.route(kPathPOST_RequestPay, methods=lstMeth_RequestPay)
def RequestPay():
    printRequestMeta(request, kPathPOST_RequestPay, lstMeth_RequestPay, request.remote_addr)
    return bst_web_request(request)
    
@app.route(kPathPOST_GetShillerInfo, methods=lstMeth_GetShillerInfo)
def GetShillerInfo():
    printRequestMeta(request, kPathPOST_GetShillerInfo, lstMeth_GetShillerInfo, request.remote_addr)
    return bst_web_request(request)

def printRequestMeta(REQUEST, URN, METHOD, CLIENT_IP):
    print('',cStrDivider02, sep='\n')
    print(__filename, f"{strUrlHit}  {REQUEST}\n{strUrnHit}  '{URN}'\n{strMethod}  {METHOD}\n{strIPAddr}  {CLIENT_IP}")

print(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .")
print(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...")
print('#======================================================================#')

