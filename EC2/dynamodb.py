import datetime as datetime

def get_data_from_dynamodb():
    try:
            import boto3
            from boto3.dynamodb.conditions import Key, Attr

            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('ambient_temp')

            startdate = datetime.date.today()

            response = table.query(
                KeyConditionExpression=Key('deviceid').eq('tempsensor1') 
                                      & Key('date_time').begins_with(str(startdate)),
                ScanIndexForward=False
            )

            items = response['Items']

            n=10 # limit to last 10 items
            data = items[:n]
            #data_reversed = data[::-1]

            return data

    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def get_daily_urfid_dynamodb():
    try:
            import boto3
            from boto3.dynamodb.conditions import Key, Attr

            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('temp_hist')

            startdate = datetime.date.today()

            response = table.query(
                KeyConditionExpression=Key('deviceid').eq('empstore')
                                      & Key('date_time').begins_with(str(startdate)),
                ScanIndexForward=False
            )

            items = response['Items']
            rfid = []
            for i in items:
                rfid.append(i['rfid'])
                
            rfid_set = set(rfid)
            return rfid_set

    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def fetch_past_rfid(rfid):
    try:
        import boto3
        from boto3.dynamodb.conditions import Key, Attr

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('temp_hist')
        
        # 10 day days prior
        startdate = (datetime.datetime.now()-datetime.timedelta(days=3)).isoformat()

        scan_kwargs= {
            'FilterExpression': Key('rfid').eq(rfid) & Key('date_time').gt(str(startdate)),
            'ProjectionExpression': "date_time, temperature"
            }
        
        response = table.scan(**scan_kwargs)
        
        items = response['Items']

        n=10 # limit to last 10 items
        data = items[:n]
        data_reversed = data[::-1]
        return data_reversed
    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def get_all_unique():
    try:
        import boto3
        from boto3.dynamodb.conditions import Key, Attr

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('temp_hist')
        scan_kwargs= {
            'FilterExpression': Key('deviceid').eq('empstore'),
            'ProjectionExpression': "rfid"
            }
        
        response = table.scan(**scan_kwargs)
        
        items = response['Items']

        out = []
        seen = []
        for line in items:
            if line['rfid'] not in seen:
                seen.append(line['rfid'])
                out.append(line)
        print(seen)
        return seen
    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])



if __name__ == "__main__":
    get_data_from_dynamodb()
