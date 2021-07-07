# Rhode Island State Payroll

The goal of this project is to collect quarterly payroll data from [transparency.ri.gov](http://www.transparency.ri.gov/payroll/). The data is cleaned and analyzed using Python to show the difference between the 2 quarters. The programs is a CLI and prints out the final results for desired departments in the prompt.

## Prerequisites

You must have **Python 3** installed.  You can download it
[here](https://www.python.org/downloads/).  

## Usage

Code is run from the command line a department is required.<br>

**--department** a state of RI department.<br>
Optional **--all** to see breakdown for all departments.

example: `python main.py --department ridoh bhddh ric ccri dot`

example: `python main.py --all`

## Department Lookup

<details>
    <summary><b>Department Lookup List</b></summary>
    <br>
    <table>
        <tr><td>lookup_name</td><td>department_name</td></tr>
        <tr><td>admin</td><td>Dept of Administration</td></tr>
        <tr><td>atomic</td><td>Atomic Energy Commission</td></tr>
        <tr><td>ag</td><td>Attorney General</td></tr>
        <tr><td>bhddh</td><td>Behavioral Health, Dev Disabilities</td></tr>
        <tr><td>boe</td><td>Board of Elections</td></tr>
        <tr><td>dbr</td><td>Business Regulations</td></tr>
        <tr><td>crmc</td><td>Costal Resources Management Council</td></tr>
        <tr><td>child</td><td>Child Advocate</td></tr>
        <tr><td>dcyf</td><td>Children & Families</td></tr>
        <tr><td>comm_deaf</td><td>Comm on Deaf/Hearing</td></tr>
        <tr><td>comm_dis</td><td>Comm on Disabilities</td></tr>
        <tr><td>comm_hr</td><td>Commission on Human Rights</td></tr>
        <tr><td>ccri</td><td>Community College of RI</td></tr>
        <tr><td>corrections</td><td>Dept of Corrections</td></tr>
        <tr><td>dem</td><td>Dept of Enviormental Management</td></tr>
        <tr><td>dor</td><td>Dept of Revenue</td></tr>
        <tr><td>dlt</td><td>Dept of Labor & Training</td></tr>
        <tr><td>doe</td><td>Dept of Education</td></tr>
        <tr><td>riema</td><td>Emergency Management Agency</td></tr>
        <tr><td>commerce</td><td>Executive Office of Commerce</td></tr>
        <tr><td>doh</td><td>Dept of Health</td></tr>
        <tr><td>hhs</td><td>Health and Human Services</td></tr>
        <tr><td>higher_ed</td><td>Higher Education</td></tr>
        <tr><td>history</td><td>Historical Preservation</td></tr>
        <tr><td>human_services</td><td>Human Services</td></tr>
        <tr><td>judicial</td><td>Judicial</td></tr>
        <tr><td>leg</td><td>Legislative</td></tr>
        <tr><td>lg</td><td>Lieutenant Governor</td></tr>
        <tr><td>mental_health</td><td>Mental Health Advocate</td></tr>
        <tr><td>military</td><td>Military Staff</td></tr>
        <tr><td>pub_defender</td><td>Public Defender</td></tr>
        <tr><td>pub_safety</td><td>Dept of Public Safety</td></tr>
        <tr><td>pub_util</td><td>Public Utilities Commission</td></tr>
        <tr><td>ric</td><td>Rhode Island College</td></tr>
        <tr><td>ethics</td><td>Ethics Commission</td></tr>
        <tr><td>arts</td><td>Council on the Arts</td></tr>
        <tr><td>sos</td><td>Secretary of State</td></tr>
        <tr><td>dot</td><td>Dept of Transportation</td></tr>
        <tr><td>treasury</td><td>Office of the General Treasurer</td></tr>
        <tr><td>uri</td><td>University of Rhode Island</td></tr>
    </table>
</details>
