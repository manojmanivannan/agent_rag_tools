import sqlite3
import pandas as pd
import random

# Step 1: Create a connection to the SQLite database
conn = sqlite3.connect('./database/example.db')
cursor = conn.cursor()

# Step 2: Create the table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS procedures (
    procedure TEXT,
    protocol TEXT,
    interface TEXT,
    request_duration REAL,
    time_out_duration REAL
)
''')
conn.commit()

# Generate additional data
def generate_data(num_records):
    procedures = ['ActivateSIM','DeactivateSIM','RegisterDevice','DeregisterDevice','InitiateCall','TerminateCall','SendSMS','ReceiveSMS','DataSessionStart','DataSessionEnd','UpdateLocation','QueryBalance','RechargeAccount','CheckVoicemail','ChangePIN','NetworkAuthentication','RoamingActivation','RoamingDeactivation','ProvisionService','SuspendService','ResumeService','ChangePlan','AddAddon','RemoveAddon','VoLTEActivation','VoLTEDeactivation','DeviceUpgrade','ResetPassword','ViewUsage','EnableCallForwarding','DisableCallForwarding']
    protocols = ['SIP','RTP','H.323SS7','GSM','CDMA','LTE','5G NR','UMTS','IMS','VoLTE','VoIP','BGP','OSPF','MPLS','SCTP','DHCP','DNS','HTTP/2','FTP','POP3','IMAP','SMPP','DiameterRADIUS','SNMP']
    interfaces = ['A1','B2','C3','D4','E5','F6','G7','H8','I9','J10','K11','L12','M13','N14','O15','P16','Q17','R18','S19','T20','U21','V22','W23','X24','Y25','Z26','AA27','BB28']
    
    data = []
    for _ in range(num_records):
        procedure = random.choice(procedures)
        protocol = random.choice(protocols)
        interface = random.choice(interfaces)
        request_duration = round(random.uniform(80, 130), 1)
        time_out_duration = round(random.uniform(15, 35), 1)
        data.append([procedure, protocol, interface, request_duration, time_out_duration])
    
    return data

# Generate 100 records
additional_data = generate_data(100)

# Convert to pandas DataFrame
df = pd.DataFrame(additional_data, columns=['procedure', 'protocol', 'interface', 'request_duration', 'time_out_duration'])

# # Save to CSV (optional)
# df.to_csv('./database/data.csv', index=False)

# # Step 3: Load data from CSV into a pandas DataFrame
# df = pd.read_csv('./database/data.csv')

# Step 4: Insert data into the SQLite table
df.to_sql('procedures', conn, if_exists='append', index=False)

# Step 5: Verify the data was inserted
cursor.execute('SELECT * FROM procedures')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
