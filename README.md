This is the version of the expense report generating script that produces PDF's 
with expense report style listing consumptions of home charger's energies
by day between two dates : the start date of the period and the end date.

To run the script which is called 'expense_report_utils_gh_local.py', go onto the command line,
navigate to the local folder and
type 'python expense_report_utils_gh_local.py'

It will ask for the date needed to be written on the pdf as a release date on top-right corner.
Date entered should be in dd/mm/yyyy format.
If one presses ENTER, it will use today's date.

For each of the CSV's and each of the home chargers listed within each CSV, a report pdf will be generated.

To modify the report number shown on the pdf itself for each user, manually change this from the CSV accordingly, remembering 
to drag down on the report_number column so that the report number/code is consistent with each home charger user.

Note that the CSV's should be in the same format as output from the sp_generate_energy_expense stored procedure in the PII schema of the database.

