# jplag_helper
This is a simple api wrapper for jplag.

Import db.sql to setup database and table.

## Testing:
Clone repo:
`run python helper.py` (you need jplag and submissions to test this)  

## Query variables:
- language: the language of the programs
- directory: the directory they are listed in
- studentID: the studentID that you want to return in api(can be ignored for returning all)
- threshold: the threshold of how much similarity will be detected(can be ignored for default 20%)

Open a new shell and paste the below editing it to fit your directory of submissions.  
`curl localhost:5000?language=c/cpp\&directory=submissions/folder\&studentID=student\&threshold=30`
