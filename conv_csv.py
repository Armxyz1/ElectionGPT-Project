# import sqlite3
# conn = sqlite3.connect('eci_kr_2023.db')
# c = conn.cursor()
# # c.execute('''CREATE TABLE elec_data (ac_no int, ac_name_x text, regions text, caste text, locality text, district text, s_no int, candidate_name text, party text, evm_votes int, postal_votes int, votes int, vote_share double, st_name text, st_no text, ac_name_y text, constituency_code int, position double, total_votes int, margin double, margin_percent double, vote_share_percent double, margin_buckets_percent text, margin_buckets_votes text)''')
# # import pandas as pd
# # # load the data into a Pandas DataFrame
# # users = pd.read_csv('eci_kr_2023.csv')
# # # write the data to a sqlite table
# # users.to_sql('eci_kr_2023', conn, if_exists='append', index = False)
# # conn.commit()
# c.execute('''SELECT * FROM eci_kr_2023''')
# for row in c.fetchall():
#     print(row)
# conn.close()
