**Log Analysis \& Threat Detection System**



**Overview**

This project simulates a basic Security Operations Center (SOC) workflow by analyzing login logs, detecting suspicious behavior, and generating security alerts.



It focuses on identifying brute-force attacks and abnormal login patterns using Python and SQL Server.





&#x20;**Technologies**

\- Python

\- SQL Server

\- pyodbc



How It Works



**Log Simulation → Database → Detection → Scoring → Alerts**



\- Logs are generated and stored in SQL Server  

\- Failed login attempts are analyzed per IP  

\- Suspicious patterns are detected  

\- Each IP is assigned a severity level  

\- Alerts are generated with explanations  





**Screenshots**



**Detection Output**

!\[Detection Output](screenshots/detection\_output.png)

**Database Logs**

!\[Database Logs](screenshots/database\_logs.png)

**Alerts File**

!\[Alerts File](screenshots/alerts\_output.png)

**SQL Analysis**

!\[SQL Analysis](screenshots/sql\_analysis.png)



**Example Output**

CRITICAL | IP: 192.168.1.10 | Score: 8 | Reason: Brute force attack succeeded

HIGH | IP: 192.168.1.20 | Score: 3 | Reason: Repeated failed login attempts



**How to Run**

python insert\_log.py

python scoring.py



**Project Structure**

databasepro/

├── db.py

├── insert\_log.py

├── scoring.py

├── alerts\_report.txt

├── README.md

└── screenshots/



&#x20;**Key Concepts**

\- Log analysis

\- SQL querying and aggregation

\- Threat detection logic

\- Basic SOC workflow

\---

&#x20;Author

Mohamed Lamine Krina  

Cybersecurity \& Computer Engineering Student



