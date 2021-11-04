from app import ResponseHandler as Helper
from app.requests.recurr_request_schema import pause_request_schema
from app.PauseModel import PauseModel
from flask import Flask, redirect, request
from flask import current_app as app
from urllib.parse import urlencode
from json import JSONEncoder
from datetime import date
import json,urllib.parse,os, time,datetime
from jsonschema import validate, ValidationError, SchemaError
from ctypes import *

class recurrController:
# DJ saso , 3ala allah 
    def pause_recurr_game(self):
        """ pause recurr games  """
        try:
            # validate request data
            if request.method == 'GET':
                request_data = request.args
            else:
                request_data = request.get_json()
            try:

                if not request_data:
                    raise Exception("No JSON provided")

                validate(request_data, pause_request_schema)

            except Exception as e:
                return Helper.error(str(e))

            libc = CDLL("libc.dylib")
            playerId = request_data['PlyID'] if 'PlyID' in request_data else 0
            playerToken = request_data['Tkn'] if 'Tkn' in request_data else ''
            deviceId = request_data['DevID'] if 'DevID' in request_data else ''
            project_key = request_data['ProjectKey'] if 'ProjectKey' in request_data else ''
            project_secret = request_data['ProjectSecret'] if 'ProjectSecret' in request_data else ''
            # Check request data are authenticated
            # auth = PauseModel.authenticate_request_data_model(self, playerId, playerToken, deviceId)
            # if not auth:
            #   raise Exception("Session Expired. Please log out and log back in", 102)

            PID = PauseModel.validate_project_credentials_model(self, project_key, project_secret)
            if not PID['result']:
                raise Exception("Request project is not recognized")

            request_data['PID'] = PID['PID'] if 'PID' in PID else ''


            if "message" in request_data:
               raise Exception(request_data['message'])

            GmID = request_data['GmID']
            project_id = request_data['PID']
            # # get all game data details
            Ply_gm_id = []
            Ply_gm_policy_id = []
            game_data = PauseModel.GetGameData(self,GmID)
            # GAME DATA TO BE RETURNED IN JSON FORMAT
            if not game_data or game_data is None :
                   raise Exception(Helper.error("Missing Game data"))

            parent_id = int(game_data["gm_copy_id"])

            # # check the game is parent game
            # if not parent_id or parent_id < 0 :
            #     raise Exception(Helper.error(" Missing parent Id"))

            # if parent_id != GmID :
            #     raise Exception(Helper.error("Game is not a parent game"))

            # check the game is a recurr game or not
            isRecurr = game_data['gm_end_pause']
            if not isRecurr or isRecurr is None :
                   raise Exception(Helper.error("This game is not a recurr game"))

            # get the game status to know if it is paused before or not
            gm_status = game_data['gm_status']
            if not gm_status or gm_status is None :
                   raise Exception(Helper.error("Missing game status"))

            # check the game is not paused before
            is_paused = gm_status
            # if is_paused  == "pause":
            #        raise Exception(Helper.error("Game is already paused"))

            # check the children of the game to lis them
            start_date = datetime.strptime(request_data['StartDate'], '%Y-%m-%d')
            start_date = start_date.date()
            end_date = datetime.strptime(request_data['EndDate'], '%Y-%m-%d')
            end_date = end_date.date()
            # get the pause type either indefinetly or for a period
            if not end_date:
                end_date = datetime.strptime("3000-01-01", '%Y-%m-%d')
                end_date = end_date.date()

            child_gms = PauseModel.GetChildGames(self,parent_id, start_date,end_date)
            # if No children games for this parent game update pause recurr for prent game only
            # else update pause recurr parent and child games
            if not child_gms :
                pause_action = PauseModel.PauseAction(self,project_id,GmID,start_date,end_date)
                if not pause_action or pause_action is None :
                     raise Exception(Helper.error("Error occured while pausing game "))

            else:
                #handle games which paused(remove reminders, players and waitlist)
                print(len(child_gms))
                for row in child_gms:
                    Ply_gm_id.append(str(row['gm_id']))
                    Ply_gm_policy_id.append(str(row['gm_policy_id']))
                    if is_paused  == "pause":
                        row['gm_status'] = "pause"

                str1 = ','.join(Ply_gm_id)
                print(child_gms)
                PlayersData = PauseModel.GetPlayerData(self,str1)
                # if PlayersData:
                #     for player_row in PlayersData:
                #         if player_row['PlyStatus'] == "player":
                #             # RefArr = self.RefundUser(player_row['PlyID'], Ply_gm_id, Ply_gm_policy_id, '', player_row['PayType'], True, 2, False)
                #             # if RefArr['error']:
                #             #     return RefArr
                #
                #             # UPGmPly = PauseModel.UPdate_Gamem_Ply(self,Ply_gm_id,player_row['PlyID'])
                #
                #             # RemoveReminderData = PauseModel.Delete_custom_notifications(self,Ply_gm_id,player_row['PlyID'])
                #
                #             # SendMail.RemoveFrmGm($row['gm_id'], $player_row['PlyID']);
                #             print(player_row['PlyStatus'])
                #
                #         if player_row['PlyStatus'] == "waitlist":
                #             print(player_row['PlyStatus'])
                #             # SendMail::RemoveFrmGm($row['gm_id'], $player_row['PlyID']);
                #
                #         if player_row['PlyStatus'] == "guest":
                #             print(player_row['PlyStatus'])
                #             # SendMail::RemoveFrmGm($row['gm_id'], 0, $player_row['PlyID']);
                #
                #     # self::RemoveGuest($row['gm_id'], $player_row['PlyID'], false);


                    #remove game players


        except (Exception, ValueError) as e:
            return Helper.error(str(e))
        else:
            return  {
                        "Result": json.dumps(game_data, indent = 4, sort_keys = True, default = str)
                    }, 200

    #
    # def getTimezoneByLatLong(self,cur_lat,cur_long):
    #     tz = tzwhere.tzwhere()
    #     time_zone = tz.tzNameAt(float(cur_lat),float(cur_long))
    #     print(time_zone)
    #     return  time_zone
    #
    # def getUtcDatetime(self,timeZone, dateTime):
    #     utcDateTime = ''
    #     if (timeZone != '' and dateTime != ''):
    #         current_utc = datetime.datetime.utcnow()
    #         utcDateTime = current_utc.strftime('%Y-%m-%d %H-%M-%S')
    #         print(utcDateTime)
    #     return utcDateTime
    #
    # def check_player_paid_for_class(self,game_id = 0,player_id = 0):
    #     if (int(game_id) < 1 or int(player_id) < 1):
    #         return False
    #
    #     cost_data = CreateModel.check_player_paid_for_class_model(self,game_id,player_id)
    #     if ((cost_data) and (float(cost_data['classCost']) > 0)
    #         or (int(cost_data['classBundle']) > 0)
    #         and (float(cost_data['classCost'] == 0))):
    #             return True
    #     return False
    #
    # def handleClassCurrencySymbol(self,gameSymbol = "", gameCurrencyName = "", gameAttendType = "", playerCountryId = 0, gameCountryId = 0):
    #     if (not gameSymbol in ['$', '€', '£'] or (gameCurrencyName == "")):
    #         return gameSymbol
    #
    #     if (str(gameCurrencyName).lower() in ['gbp', 'eur']):
    #         return gameSymbol
    #
    #     if (gameSymbol != '$'):
    #         return str(gameCurrencyName).upper()
    #
    #     if (gameAttendType and str(gameAttendType).lower() == 'zoom'):
    #         if (int(playerCountryId) == int(gameCountryId)):
    #             return gameSymbol
    #         return str(gameCurrencyName).upper()
    #
    #     if (str(gameCurrencyName).lower() == 'usd'):
    #         return gameSymbol
    #     s = str(gameCurrencyName).upper()
    #     s = s[0: 0 + 1]
    #     return s + gameSymbol
    #
    #
    # def GetGmStatus(self,GmID = 0,project_id = 0):
    #     status = ""
    #     gmRow = CreateModel.GetGmStatusModel(self,project_id,GmID)
    #     if (gmRow):
    #         if(int(gmRow['gm_recurr_id']) > 0):
    #             parentRow = PauseModel.parentRowModel(self,project_id,gmRow['gm_recurr_id'])
    #             if(parentRow):
    #                 if((int(parentRow['gm_recurr_cancel_type']) == 1)
    #                     or (int(parentRow['gm_recurr_cancel_type']) == 2)
    #                     or (int(parentRow['gm_recurr_cancel_type']) == 3)
    #                     and gmRow['gm_status'] == 'cancel'):
    #                         status = 'cancel'
    #
    #         elif (gmRow['gm_status'] == 'cancel'):
    #             status = 'cancel'
    #     return status
    #
    # def getAllGstByGmID(self,GmID = 0):
    #     guestIDs = []
    #     gstData = PauseModel.gstDataModel(self,GmID)
    #     if (gstData):
    #         guestIDs =  [IDS.get('guest_ply_id') for IDS in gstData]
    #
    #     return guestIDs
    #
    # def getGmInstructorData(self,GmID = 0, GmRecurID = 0, for_recur_only = False):
    #     data = []
    #     result = []
    #     sql = ''
    #     #get instructor if set for this class only in parent table
    #     if (for_recur_only == False):
    #         sql = """
    #                 SELECT instructor_id, name, bio, image
    #                 FROM gm_instructors_parents_only
    #                 JOIN instructors
    #                 ON instructors.id = gm_instructors_parents_only.instructor_id
    #                 WHERE gm_id = %s
    #                 """
    #         sql = sql % (GmID)
    #
    #         data = PauseModel.gm_instructors_parents_only_model(self,sql)
    #
    #     #get instructor data from general table
    #     if (not data):
    #         sql = """
    #                 SELECT instructor_id, name, bio, image
    #                 FROM gm_instructors
    #                 JOIN instructors ON instructors.id = gm_instructors.instructor_id
    #                 WHERE gm_id = %s
    #                 """
    #         sql = sql % (GmID)
    #         data = PauseModel.gm_instructors_model(self,sql)
    #
    #     #get instructor for class from its parent class in general table
    #     if (not data):
    #         #get data from game parent
    #         parentID = Game.getGmParentID(self,GmID, GmRecurID)
    #         #prepare query
    #         query = sql % parentID
    #         data = PauseModel.gm_instructors_parents_only_model_data(self,sql)
    #         if (not data):
    #             return result
    #
    #     #handle returned results
    #     aDict = dict()
    #     aDict['id'] = int(data['instructor_id'])
    #     aDict['name'] = data['name']
    #     aDict['bio'] = data['bio']
    #     aDict['image'] = data['image']
    #     result.append(aDict)
    #
    #     return result
    #
    #
    # def chkNofeesPayed(self,GmID = 0, PlyID = 0, GmFees = 0):
    #     try:
    #         afterDis = ""
    #         NofeesPayed = False
    #         libc = CDLL("libc.dylib")
    #         couponData = PauseModel.chkNofeesPayedSql(self,GmID,PlyID)
    #
    #         if (couponData):
    #             if (libc.strcasecmp(couponData['type'], 'p') == 0):
    #                 afterDis = GmFees - (GmFees * couponData['discount'] / 100)
    #             elif(libc.strcasecmp(couponData['type'], 'f') == 0):
    #                 afterDis = GmFees - couponData['discount']
    #
    #             if (int(afterDis) <= 0):
    #                 NofeesPayed = True
    #
    #     except (Exception, ValueError) as e:
    #         return Helper.error(str(e))
    #     else:
    #         return NofeesPayed
    #
    # def CountGmPlys(self,GmID = 0):
    #     try:
    #         GmPlys = 0
    #         GmPlysWhere = ""
    #         #get all guests then count all the players who are not in guest table.
    #         AllGuests = self.getAllGstByGmID(self,GmID)
    #         print(AllGuests)
    #         if (AllGuests):
    #             GmPlysWhere = " AND gm_ply_ply_id NOT IN (%s)"
    #             # jo = ",".join(AllGuests)
    #             jo = ','.join(str(v) for v in AllGuests)
    #             GmPlysWhere = GmPlysWhere % jo
    #
    #         GmPlysRow = PauseModel.GmPlysRowCountModel(self,GmID,GmPlysWhere)
    #         if (GmPlysRow):
    #             GmPlys = GmPlysRow['GmPlys']
    #
    #         GmGsts = 0
    #         GmGstsRow = PauseModel.GmGstsRowModel(self,GmID)
    #         if (GmGstsRow):
    #             GmGsts = GmGstsRow['guestsNum']
    #     except (Exception, ValueError) as e:
    #         return Helper.error(str(e))
    #     else:
    #         return str(GmPlys + GmGsts)
    #
    # def getAllGstByGmID(self,GmID = 0):
    #     try:
    #         guestIDs = []
    #         gstData = PauseModel.gstDataModel(self,GmID)
    #         if (gstData):
    #             guestIDs =  [IDS.get('guest_ply_id') for IDS in gstData]
    #     except (Exception, ValueError) as e:
    #         return Helper.error(str(e))
    #     else:
    #         return guestIDs
    #
    # def logAllActions(self,logData):
    #     try:
    #         print("m.dsmmdsmn")
    #         if not logData:
    #             return 0
    #
    #         UserId = logData['UserId'] if ('UserId' in logData and logData['UserId']) else 0
    #         GmID = logData['GmID'] if ('GmID' in logData and logData['GmID']) else 0
    #         SubscriptionId = logData['SubscriptionId'] if ('SubscriptionId' in logData and logData['SubscriptionId']) else 0
    #         OrgId = logData['OrgId'] if ('OrgId' in logData and logData['OrgId']) else 0
    #         PayType = logData['PayType'] if ('PayType' in logData and logData['PayType']) else ''
    #         Cost = float(logData['Cost']) if ('Cost' in logData and logData['Cost']) else 0
    #         CouponCode = logData['CouponCode'] if ('CouponCode' in logData and logData['CouponCode']) else ''
    #         Note = logData['Note'] if ('Note' in logData and logData['Note']) else ''
    #         PolicyId = logData['PolicyId'] if ('PolicyId' in logData and logData['PolicyId']) else 0
    #         IsMedical = logData['IsMedical'] if ('IsMedical' in logData and logData['IsMedical']) else 0
    #         SrcType = logData['SrcType'] if ('SrcType' in logData and logData['SrcType']) else ''
    #         LogType = logData['LogType'] if ('LogType' in logData and logData['LogType']) else 0
    #         ContactId = logData['ContactId'] if ('ContactId' in logData and logData['ContactId']) else 0
    #         CurrencySymbol = logData['CurrencySymbol'] if ('CurrencySymbol' in logData and logData['CurrencySymbol']) else ''
    #
    #         InsActionLog = PauseModel.logAllActionsModel(self,UserId,GmID,SubscriptionId,OrgId,
    #                                                       PayType,Cost,CouponCode,Note,PolicyId,
    #                                                  IsMedical,SrcType,LogType,ContactId,CurrencySymbol)
    #     except (Exception, ValueError) as e:
    #         return Helper.error(str(e))
    #     else:
    #         return InsActionLog
    #
    # def RemoveNulls(self,Arr = []):
    #    try:
    #         is_array = lambda var: isinstance(var, (list, tuple, set))
    #         if (not is_array(Arr) or len(Arr) == 0):
    #             return Arr
    #         Arr = str(Arr).encode().decode('utf-8')
    #         Arr = json.dumps(Arr).encode('utf-8')
    #         Arr = str(Arr).replace(":null", ':""')
    #    except (Exception, ValueError) as e:
    #         return Helper.error(str(e))
    #    else:
    #         return json.dumps(Arr, sort_keys=True)
    #
    # def RefundUser(self,PlyID,child_gms,RefundType,appSource,payType,EditPlayerCredit,isWithdraw,isBan,PID):
    #     try:
    #         ResArr = []
    #         GmID = child_gms['gm_id']
    #         Fees = child_gms['Fees']
    #         GameSubscription = []
    #         PayType = child_gms['PayType']
    #         OrgID = child_gms['OrgID']
    #         PolicyID = child_gms['PolicyID']
    #         PolicyT = child_gms['PolicyT']
    #         GmMaxPly = int(child_gms['MaxPly'])
    #         GmUTCDate = child_gms['UTCDateTime']
    #         GameRefundable = True
    #         showMoreLink = 'False'
    #         WithSuccMess = "You have withdrawn from this class."
    #         noteText = ''
    #         AmountRefund = 0
    #         isRefunded = False
    #         libc = CDLL("libc.dylib")
    #         os.environ['UTC'] = 'Europe/Berlin'  # change accordingly
    #         time.tzset()
    #         today = date.today()
    #         currDate = today.strftime("%Y-%m=%d %h:%i:%s")
    #         hourdiff = round((datetime.datetime.strptime(GmUTCDate) - datetime.datetime.strptime(currDate))/3600, 1)
    #         # if the policy is full refund (24 hours) , check if the game will start less than 24 hours , so there is no refund.
    #         if (int(PolicyID) == 5 and  hourdiff < 24 and isWithdraw == 1):
    #             GameRefundable =  False
    #             noteText = "User has been no refund because the policy is full refund before(24 hours) , but the game will start less than 24 hours"
    #
    #         # if the policy is full refund (1 hour) , check if the game will start less than 1 hour , so there is no refund.
    #         elif (int(PolicyID) == 6 and  hourdiff < 1 and isWithdraw == 1):
    #             GameRefundable =  False
    #             noteText = "User has been no refund because the policy is full refund before(1 hour) ,but the game will start less than 1 hour"
    #
    #         # if the policy is full refund (3 hours) , check if the game will start less than 3 hours , so there is no refund.
    #         elif (int(PolicyID) == 7 and  hourdiff < 3 and isWithdraw == 1):
    #             GameRefundable =  False
    #             noteText = "User has been no refund because the policy is full refund before(3 hours) ,but the game will start less than 3 hours"
    #
    #         # if the policy is full refund (6 hours), check if the game will start less than 6 hours , so there is no refund.
    #         elif (int(PolicyID) == 8 and hourdiff < 6 and isWithdraw == 1):
    #             GameRefundable =  False
    #             noteText = "User has been no refund because the policy is full refund before(6 hours),but the game will start less than 6 hours"
    #
    #         # if the policy is full refund (12 hours), check if the game will start less than 12 hours , so there is no refund
    #         elif (int(PolicyID) == 9 and  hourdiff < 12 and isWithdraw == 1):
    #             GameRefundable =  False
    #             noteText = "User has been no refund because the policy is full refund before(12 hours), but the game will start less than 12 hours"
    #
    #         # if the policy is full refund (48 hours), check if the game will start less than 48 hours , so there is no refund .
    #         elif (int(PolicyID) == 10 and  hourdiff < 48 and isWithdraw == 1):
    #             GameRefundable =  False
    #             noteText = "User has been no refund because the policy is full refund before(48 hours), but the game will start less than 48 hours"
    #
    #         if (int(PolicyID) >= 5):
    #             noteText = "You have withdrawn from this class."
    #
    #
    #         # Check first if this player has subscriptions with this game admin or not
    #         GameSubscription = self.GetGameSubscription(self,GmID,PlyID)
    #         checkGmJoinedBundle = self.check_joined_class_with_bundle(self,GmID,PlyID)
    #
    #         if ((GameSubscription and GameSubscription['joinType'] and GameSubscription['joinType'] != 'discount') or EditPlayerCredit == False or checkGmJoinedBundle):
    #         # This player payed this game with plan, so increase this plan credit if game is refundable
    #
    #             plyCredit = True
    #
    #             GmPlys = self.CountGmPlys(self,GmID)
    #             if (int(PolicyID) == 1 and int(isWithdraw) == 1 and int(GmPlys) >= int(GmMaxPly)):
    #                 # // Policy =1 (Refund if replaced)  so chkeck if game players less than the game max player
    #                 # // if there is still space for others to join, so refund.
    #                 GameRefundable = False
    #                 noteText = "Refunds IF Replaced"
    #             elif (int(PolicyID) == 2 and int(isWithdraw) == 1):
    #                 GameRefundable = False
    #                 noteText = "No Refunds Policy"
    #             elif (EditPlayerCredit and GameRefundable):
    #                 SubID = int(GameSubscription['SubID'])
    #                 # plyCredit = self.EditPlayerCredit(self,SubID,PlyID, '+', '', GmID)
    #                 noteText = "User has been refunded via class credit"
    #
    #
    #             # Remove Game Plan From DB
    #             plyGmSub = False
    #             if (GameRefundable == True):
    #                 plyGmSub = self.RemoveGameSubscription(self,GmID,PlyID)
    #
    #             if (plyCredit == True and plyGmSub == True and GameRefundable == True):
    #                 GmPlyRefund = PauseModel.GmPlyRefundSql(self,PlyID,GmID)
    #                 isRefunded = True
    #
    #             ResArr = dict['Result' : "True"]
    #
    #         else:
    #             # This player paid this game only, so refund the money back
    #             # and the player is not added as aguest.
    #             # refund player if he is not a guest.
    #             guestData = PauseModel.guestDataSql(self,PlyID,GmID)
    #
    #             # check if player paid to join class
    #             check_cost = PauseModel.check_player_paid_for_class_sql(self,PlyID,GmID)
    #
    #             # complete refund
    #             if (child_gms['IsFree'] == 'n' and float(child_gms['Fees']) > 0 and libc.strcasecmp(child_gms['PayType'], 'stripe') == 0 and not guestData and check_cost):
    #                 GetData = PauseModel.GetDataSql(self,PlyID,GmID)
    #                 if (GetData and int(GetData['gm_ply_refunded']) == 0):
    #                     Policy = 0
    #                     if (int(RefundType) == 0):
    #                         Policy = 5  # to make a full refund in case of game cancel or remove a player.
    #                         noteText = "to make a full refund in case of game cancel or remove a player."
    #                         GameRefundable = True # // to make full refund in case of gm cancelled.
    #                     else:
    #                         Policy = GetData['gm_policy_id']
    #
    #                     if (GameRefundable == True):
    #                         GmPlys = self.CountGmPlys(self,GmID)
    #                         # // -- Policy = 1(Refund if replaced) so chkeck if game players less than the game max player
    #                         # // -- if there is still space for others to join, so refund.
    #                         if (int(Policy) != 1 or (int(Policy) == 1 and (GmPlys < GmMaxPly)) or int(isWithdraw) != 1):
    #                             # // ---- Withdraw Message depending on policy and if game is full or not.
    #                              if (int(Policy) == 3):
    #                                 noteText = "User has been refunded with 50% refunded"
    #                              elif (int(Policy) != 2):
    #                                 # // if the policy is not 'No Refund'.
    #                                 noteText = "User has been fully refunded"
    #
    #                              if (int(Policy) == 2):
    #                                 noteText = "This policy No Refund"
    #
    #                             # // get currency
    #                              CurrencyData = PauseModel.CurrencyDataSql(self,GmID)
    #                              if (int(Policy) != 2 or (int(Policy) == 2 and int(isWithdraw) != 1)):
    #                                 # // make refund
    #                                 if (libc.strcasecmp(payType, 'direct') == 0):
    #                                     refund_action = self.DirectRefund(self,GmID,PlyID,isWithdraw)
    #                                 else:
    #                                     refund_action = self.MakeRefund(self,GmID,PlyID,isWithdraw)
    #
    #                                 if ((refund_action["Result"]) and refund_action["Result"] == "True"):
    #                                     isRefunded = True
    #
    #                                 ResArr = dict["Result" : "True"]
    #                              else:
    #                                 ResArr = dict['Result':"True"]
    #
    #
    #                              refund_condition = ''
    #                              if isRefunded:
    #                                 refund_condition = 'gm_ply_refunded = 1'
    #                              else:
    #                                 refund_condition = 'gm_ply_refunded = 0'
    #
    #                              sql = PauseModel.gm_playersSql(self,refund_condition,PlyID,GmID)
    #                         else:
    #                             if (int(Policy) == 1 and (GmPlys >= GmMaxPly)):
    #                                 ResArr = dict['Result' :"True"]
    #                                 noteText = "User will be refunded if someone else takes your spot"
    #
    #
    #
    #                 elif(int(PolicyID) == 1):
    #                     # this part is created in the case of( if replaced withdarw policy),
    #                     # if the user joined
    #                     # with coupon 100 % then the amount to pay is 0, So in case of withdraw we need to make the refunded column
    #                     # in the gm_players talble =1, so when he joins again with no coupons  he will be charged normally.
    #
    #                     noFees = self.chkNofeesPayed(self,GmID, PlyID,Fees)
    #                     if (noFees == True):
    #                         refund_condition = 'gm_ply_refunded = 1'
    #                         sql = PauseModel.gm_playersSql(self, refund_condition, PlyID, GmID)
    #
    #                     ResArr = dict['Result' : "True"]
    #
    #         # append withdraw success message to result in success case
    #         if (not ResArr['error'] and WithSuccMess):
    #             ResArr["WithSuccMess"] = WithSuccMess
    #             ResArr["showMoreLink"] = showMoreLink
    #
    #         # main log action client withdraw from a game
    #
    #         logData = []
    #         pay_amount = 0
    #         amountRefund = 0
    #         [amountRefund, pay_amount] = self.get_game_refund_amounts(self,GmID, PlyID)
    #         couponData = PauseModel.couponDataSql(self,GmID,PlyID)
    #         currenciesData = PauseModel.currenciesDataSql(self,GmID)
    #
    #         isBundle = 0
    #         logData['UserId'] = PlyID
    #         logData['GmID'] = GmID
    #         logData['OrgId'] = child_gms['OrgID']
    #         logData['PayType'] = child_gms['PayType']
    #         logData['Cost'] = pay_amount
    #         logData['CouponCode'] = couponData['couponCode'] if couponData['couponCode'] else ''
    #
    #         costRefund = 0
    #         currencySymbol = currenciesData['currency_symbol'] if currenciesData['currency_symbol']  else ''
    #         costRefund = str(currencySymbol) + str(amountRefund)
    #
    #         if (guestData):
    #             LogNote = "addedAsClient" #"User has been refunded by the admin. No refund is due as per refund policy"
    #             logData['Cost'] = 0
    #             logData['PayType'] = ""
    #         elif (GameSubscription['SubID']):
    #             logData['SubscriptionId'] = GameSubscription['SubID']
    #             subName = GameSubscription['SubName'] if GameSubscription['SubName'] else ""
    #
    #             if (isRefunded):
    #                 LogNote = "User has been refunded with a class credit as per refund policy"
    #             else:
    #                 LogNote = "User has not been refunded as per refund policy"
    #
    #
    #             logData['Cost'] = 0
    #             logData['PayType'] = ""
    #             isBundle = 1
    #
    #         elif(child_gms['PayType'] and libc.strcasecmp(child_gms['PayType'], "onsite") == 0 and child_gms['IsFree'] == 'n'):
    #             if (isRefunded):
    #                 if (int(amountRefund) > 0):
    #                     LogNote = "User has been refunded via Stripe as per refund policy"
    #                 else:
    #                     LogNote = "No refund was due as the user did not pay to join the class."
    #             elif(logData['CouponCode'] != '' and int(amountRefund) == 0):
    #                 LogNote = "No refund was due as the user did not pay to join the class."
    #             else:
    #                 LogNote = "User has not been refunded via Stripe as per refund policy"
    #
    #         elif(child_gms['IsFree'] == 'y'):
    #             LogNote = ''
    #         elif(child_gms['PayType'] and libc.strcasecmp(child_gms['PayType'], "Stripe") == 0 and child_gms['IsFree'] == 'n' and int(isBundle) == 0):
    #             if (isRefunded):
    #                 if (int(amountRefund) > 0):
    #                     LogNote = "User has been refunded by the admin and refunded as per refund policy"
    #                 else:
    #                     LogNote = "User has been refunded by the admin. No refund is due as per refund policy."
    #
    #         elif(logData['CouponCode'] != '' and int(amountRefund) == 0):
    #             LogNote = "User has been refunded by the admin. No refund is due as per refund policy"
    #         else:
    #             LogNote = "User has not been refunded via Stripe as per refund policy"
    #
    #
    #
    #         logData['SrcType'] = appSource
    #         if (int(isWithdraw) == 1 and int(isBan) == 0):
    #             logData['Note'] = LogNote
    #             logData['LogType'] = 4
    #
    #
    #         # log action admin banned user
    #         if (int(isBan) == 1):
    #             logData['Note'] = " User got banned.\n" + LogNote
    #             logData['LogType'] = 12
    #
    #         # log action admin removed user from class
    #         if (int(isWithdraw) == 2):
    #             logData['Note'] = LogNote
    #             logData['LogType'] = 12
    #
    #         self.logAllActions(self,logData)
    #         ResArr = self.RemoveNulls(self,ResArr)
    #
    #     except (Exception, ValueError) as e:
    #         return Helper.error(str(e))
    #     else:
    #         return ResArr
