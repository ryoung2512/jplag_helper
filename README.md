# jplag_helper
Simple api wrapper for jplag.

Import db.sql to setup database and table.

Testing:
Clone repo:
run python helper.py (you need jplag and submissions to test this)

Open a new shell and paste the below editing it to fit your directory of submissions.
curl localhost:5000?language=c/cpp\&directory=submissions/folder
