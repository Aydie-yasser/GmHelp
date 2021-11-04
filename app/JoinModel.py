from app import ResponseHandler as Helper
from database.DBConnector import DBConnector

class PauseModel:

    def GetGameData(self, GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = "SELECT * FROM game WHERE gm_id = %s"
            gmSql = gmSql % (GmID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()



    def gm_playersSql(self, refund_condition,PlyID,GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = """
                    UPDATE gm_players SET "%s"
                    WHERE gm_ply_ply_id = "%s"
                    AND gm_ply_gm_id = %s
                    """

            gmSql = gmSql % (refund_condition,PlyID,GmID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def CurrencyDataSql(self, GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = """
                        SELECT currency_name , currency_symbol
                        FROM game LEFT JOIN currencies ON currency_id=gm_currency_symbol
                        WHERE gm_id = '%s'
                        """

            gmSql = gmSql % (GmID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def GmPlyRefundSql(self,PlyID, GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = """
                            UPDATE gm_players SET gm_ply_refunded=1
                            WHERE gm_ply_ply_id="%s"
                             AND gm_ply_gm_id = %s"
                            """

            gmSql = gmSql % (PlyID,GmID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def guestDataSql(self,PlyID, GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = "SELECT * FROM guests WHERE guest_ply_id=%s AND guest_gm_id=%s"

            gmSql = gmSql % (PlyID,GmID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()



    def check_player_paid_for_class_sql(self,PlyID, GmID):
        if (int(GmID) < 1 or int(PlyID) < 1):
            return False
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = """
                SELECT actions_log_cost AS classCost
                FROM actions_log
                WHERE actions_log_class_id = %s
                AND actions_log_user_id = %s
                AND actions_log_action_type_id = 1
                ORDER BY actions_log_datetime DESC
                """

            gmSql = gmSql % (GmID,PlyID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:

            if mysql_cursor.rowcount:
                if float(gameData['classCost']) > 0:
                    return True
                else:
                    return False
            return False
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()


    def gstDataModel(self,GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gstSQl = """
                    SELECT guest_ply_id FROM guests
                     WHERE guest_ply_id !=0 
                     AND guest_gm_id = %s
                     """

            gstSQl = gstSQl % (GmID)
            print(gstSQl)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gstSQl)
            gstData = mysql_cursor.fetchall()
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gstData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()


    def chkNofeesPayedSql(self,GmID,PlyID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gstSQl = """
                    SELECT * FROM coupon_uses
                    LEFT JOIN coupons ON coupon_uses.coupon_id = coupons.id
                    WHERE gm_id = "%s"
                    AND ply_id = "%s"
                    ORDER BY coupon_uses.updated_at DESC
                    """
            gstSQl = gstSQl % (GmID,PlyID)
            print(gstSQl)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gstSQl)
            gstData = mysql_cursor.fetchone()
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gstData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def couponDataSql(self,GmID,PlyID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gstSQl = """
                        SELECT coupons.code AS couponCode FROM coupon_uses
                         LEFT JOIN coupons ON coupon_uses.coupon_id = coupons.id
                        WHERE gm_id = "%s"
                        AND ply_id = "%s"
                        ORDER BY coupon_uses.updated_at DESC
                        """

            gstSQl = gstSQl % (GmID,PlyID)
            print(gstSQl)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gstSQl)
            gstData = mysql_cursor.fetchone()
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gstData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def currenciesDataSql(self,GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gstSQl = """
                            SELECT currency_name , currency_symbol FROM game
                            LEFT JOIN currencies ON currency_id = gm_currency_symbol
                            WHERE gm_id = '%s'
                            """

            gstSQl = gstSQl % (GmID)
            print(gstSQl)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gstSQl)
            gstData = mysql_cursor.fetchone()
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gstData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()


    def logAllActionsModel(self,UserId,GmID,SubscriptionId,OrgId,PayType,Cost,
                   CouponCode,Note,PolicyId,IsMedical,SrcType,LogType,ContactId,
                   CurrencySymbol):
        mysql_cursor = None
        mysql_connection = None
        try:
            InsActionLog = """
                        INSERT INTO actions_log 
                        (actions_log_user_id ,
                        actions_log_class_id ,
                        actions_log_subscription_id ,
                        actions_log_org_id ,
                        actions_log_payment_type ,
                        actions_log_cost ,
                        actions_log_coupon_code,
                        actions_log_note, 
                        actions_log_policy_id,
                        actions_log_is_medical,
                        actions_log_src_type,
                        actions_log_action_type_id,
                        actions_log_contact_id,
                        actions_log_currency_symbol)
                        VALUES('"%s"','"%s"','"%s"','"%s"',
                                '"%s"','"%s"','"%s"','"%s"',
                                '"%s"','"%s"','"%s"', '"%s"',"%s",'"%s"')

            """
            InsActionLog = InsActionLog % (UserId,GmID,SubscriptionId,OrgId,PayType,Cost,
                   CouponCode,Note,PolicyId,IsMedical,SrcType,LogType,ContactId,
                   CurrencySymbol)
            print(InsActionLog)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(InsActionLog)
            PlyInfo = mysql_cursor.lastrowid
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return PlyInfo
            return int()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()


    def GmGstsRowModel(self,GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            GmGstsSql = """
                        SELECT COUNT(guest_gm_id) AS guestsNum
                         FROM guests WHERE guest_gm_id='%s'
                         """

            GmGstsSql = GmGstsSql % (GmID)
            print(GmGstsSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(GmGstsSql)
            GmGstsRow = mysql_cursor.fetchone()
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return GmGstsRow
            return dict()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def GmPlysRowCountModel(self,GmID,GmPlysWhere):
        mysql_cursor = None
        mysql_connection = None
        try:
            GmPlysSql = """
                            SELECT COUNT(gm_ply_ply_id) AS GmPlys
                            FROM gm_players
                            WHERE gm_ply_status = 'y'
                            AND gm_ply_gm_id ='%s' %s
                        """

            GmPlysSql = GmPlysSql % (GmID,GmPlysWhere)
            print(GmPlysSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(GmPlysSql)
            GmPlysRow = mysql_cursor.fetchone()
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return GmPlysRow
            return dict()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()


    def GetDataSql(self,PlyID, GmID):
        mysql_cursor = None
        mysql_connection = None
        try:
            gmSql = """ 
                    SELECT gm_id, gm_policy_id, gm_ply_refunded
                    FROM game JOIN gm_players ON gm_id = gm_ply_gm_id
                    WHERE gm_id = %s
                    AND gm_ply_ply_id= %s
                    """

            gmSql = gmSql % (GmID,PlyID)
            print(gmSql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(gmSql)
            gameData = mysql_cursor.fetchone()
            print(gameData)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def GetChildGames (self, GmID ,StartDate, EndDate):
        mysql_cursor = None
        mysql_connection = None

        try :
            if StartDate is None :
                raise ValueError("Invalid Start date ")

            if EndDate is None:
                raise ValueError("Invalid End Date")

            if StartDate > EndDate :
                raise ValueError("Start Date cannot be greater than End Date")

            ss = str(StartDate)
            dd = str(EndDate)
            pause_date_limits_sql = """
                                    SELECT gm_id, gm_status,gm_policy_id FROM game 
                                    WHERE  gm_recurr_id = %s
                                     AND gm_date between %s AND '%s'
                                    """

            pause_date_limits_sql = pause_date_limits_sql % (GmID ,StartDate,EndDate)
            print(pause_date_limits_sql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(pause_date_limits_sql)
            child_data = mysql_cursor.fetchall()
            # print(child_data)

        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return child_data
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def GetPlayerData(self,GmID):
        mysql_cursor = None
        mysql_connection = None

        try :
            PlayersSQl = """ 
                    SELECT gm_ply_ply_id AS PlyID,
                    gm_ply_pay_type AS PayType,
                    'player' AS PlyStatus
                    FROM gm_players
                    WHERE gm_ply_gm_id IN (%s)
                    AND gm_ply_status = 'y'
                    UNION SELECT gm_wait_list_ply_id AS PlyID,
                    '' AS PayType,
                    'waitlist' AS PlyStatus
                    FROM gm_waitlist
                    WHERE gm_wait_list_gm_id IN (%s)
                    AND gm_wait_list_withdrew = 0
                    AND gm_wait_list_removed_by_admin = 0
                    UNION SELECT guest_id AS PlyID,
                    '' AS PayType,
                    'guest' AS PlyStatus
                    From guests
                    WHERE guest_gm_id IN (%s)
                    AND guest_ply_id = 0
                    """
            PlayersSQl = PlayersSQl % (GmID,GmID,GmID)
            print(PlayersSQl)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(PlayersSQl)
            gameData = mysql_cursor.fetchall()
            print(gameData)

        except (Exception, ValueError)as e:
            raise Exception(str(e))

        else:
            if mysql_cursor.rowcount:
                return gameData
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def PauseAction(self,project_id,GmID,start_date,end_date):
        mysql_cursor = None
        mysql_connection = None

        try:
            datePaused = start_date + "_" + end_date
            pause_date_limits_sql = """
                        UPDATE game SET gm_end_pause = '%s' 
                        WHERE gm_pid = '%s' AND gm_id = '%s'
                 """

            pause_date_limits_sql = pause_date_limits_sql % (datePaused, project_id, GmID)
            print(pause_date_limits_sql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(pause_date_limits_sql)
            child_data = mysql_cursor.fetchall()
            print(child_data)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return child_data
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def UPdate_Gamem_Ply(self,gm_id,PlyID):
        mysql_cursor = None
        mysql_connection = None

        try:
            pause_date_limits_sql = """
                                UPDATE gm_players SET
                                gm_ply_status = 'r',
                                gm_ply_leave = CURRENT_TIMESTAMP,
                                gm_ply_removed_by_admin = 1
                                WHERE gm_ply_gm_id = "%s"
                                AND gm_ply_ply_id = %s"
                            """
            pause_date_limits_sql = pause_date_limits_sql % (gm_id,PlyID)
            print(pause_date_limits_sql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(pause_date_limits_sql)
            child_data = mysql_cursor.fetchall()
            print(child_data)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return child_data
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def Delete_custom_notifications(self,gm_id,PlyID):
        mysql_cursor = None
        mysql_connection = None

        try:
            pause_date_limits_sql = """
                                    DELETE FROM custom_notifications
                                    WHERE custom_notification_gm_id= "%s"
                                    AND custom_notification_ply_id = %s
                                 """
            pause_date_limits_sql = pause_date_limits_sql % (gm_id,PlyID)
            print(pause_date_limits_sql)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(pause_date_limits_sql)
            child_data = mysql_cursor.fetchall()
            print(child_data)
        except (Exception, ValueError)as e:
            raise Exception(str(e))
        else:
            if mysql_cursor.rowcount:
                return child_data
            return list()
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()




    def validate_project_credentials_model(self,project_key, project_secret):
        """
        Validate project key and secret
        """
        mysql_cursor = None
        mysql_connection = None
        try:
            if project_key == '':
                raise ValueError('invalid Project Key')
            if project_secret == '':
                raise ValueError('invalid Project Secret')
            query = """
                    SELECT project_id
                    FROM projects
                    WHERE project_key = "%s"
                    AND project_secret = "%s"
                    """
            query = query % (project_key, project_secret)
            print(query)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(query)
            PID = mysql_cursor.fetchone()
            print(PID)

        except (Exception, ValueError)as e:
            return Helper.error(str(e))
        else:
            if mysql_cursor.rowcount:
                return {"result": True, "PID": PID}
            else:
                return {"result": False, "PID": PID}
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

    def authenticate_request_data_model(self,playerId, playerToken, deviceId):
        mysql_cursor = None
        mysql_connection = None
        try:
            if int(playerId) < 1:
                raise ValueError("Invalid Player Id")
            if type(playerToken) != str or len(playerToken) < 1 or playerToken == "":
                raise ValueError("Invalid Player Token")
            if type(deviceId) != str or len(deviceId) < 1 or deviceId == "":
                raise ValueError("Invalid Device Id")
            query = """
                        SELECT ply_tkn_gcm_id
                        FROM ply_tkn_gcm
                        WHERE ply_tkn_gcm_ply_id = %s
                            AND ply_tkn_gcm_token = "%s"
                            AND ply_tkn_gcm_dev = "%s"
                        """
            query = query % (playerId, playerToken, deviceId)
            db_connector = DBConnector()
            (mysql_connection, mysql_cursor) = db_connector.db_connection_factory('old', 'read')
            mysql_cursor.execute(query)
            mysql_cursor.fetchone()
        except (Exception, ValueError) as e:
            return Helper.error(str(e))
        else:
            if mysql_cursor.rowcount:
                return True
            else:
                return False
        finally:
            if mysql_cursor and mysql_connection:
                mysql_cursor.close()
                mysql_connection.close()

