# Premier League data
Statistics and standings from my favorite football league. 

### Process

Several Python scripts collect data on past and current results, including: 

**Season results**
- Current table (live): `fetch_current_table.py`
    - *Automated with Github Actions workflow* 
    - *Runs twice daily to capture fixures on odd days during periods of European and international play* 
- Past tables (historical): `fetch_past_tables.py`
    - *Output stored on S3*
    - *Used for reference*

### Outputs

**Season results tables**
- Historical (1992/93-2023/24): [JSON](https://stilesdata.com/football/table/epl_table_past.json), [CSV](https://stilesdata.com/football/table/epl_table_past.csv)
- Latest (2024-24): [JSON](), [CSV]()




*More to come...*