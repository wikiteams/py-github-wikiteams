py-github-wikiteams
===================

This software is available to public

Copyright (C) 2013 - WikiTeams contributors

py-github-wikiteams is for free. You don't have to pay for it, and you can use it any way you want. It is developed as an Open Source project under the GNU General Public License (GPL). That means you have full access to the source code of this program. You can find it on our website at https://github.com/wikiteams/py-github-wikiteams Should you wish to modify or redistribute this program, or any part of it, you should read the full terms and conditions set out in the license agreement before doing so. A copy of the license is available on our website. If you simply wish to install and use this software, you need only be aware of the disclaimer conditions in the license, which are set out below. NO WARRANTY Because the program is licensed free of charge, there is no warranty for the program, to the extent permitted by applicable law. Except when otherwise stated in writing the copyright holders and/or other parties provide the program "as is" without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the program is with you. Should the program prove defective, you assume the cost of all necessary servicing, repair or correction. In no event unless required by applicable law or agreed to in writing will any copyright holder, or any other party who may modify and/or redistribute the program as permitted above, be liable to you for damages, including any general, special, incidental or consequential damages arising out of the use or inability to use the program (including but not limited to loss of data or data being rendered inaccurate or losses sustained by you or third parties or a failure of the program to operate with any other programs), even if such holder or other party has been advised of the possibility of such damages.

This script allows to get details of "most popular repositories" using GitHub API

Input of program are CSV files with: `name`, `owner`, `forks`, `watchers`

In data there are around 27.000 repositories parsed from Google BigQuery (as on 15.09.2013)

On output you get CSV files with below dimensions:

1. Repository size 
2. Commits count
3. Commit count in particular skill (multiple variables) 
4. Star count (indicator of team quality)
5. Notifications count (number of people receiving notifications)
6. Count of issues grouped by issue type
7. Number of people in particular role ( Issuer -> Wiki(other content)  -> Developer (commit) -> Owner)
8. Median of issue closure team grouped by issue type
9. Count of Unwatch events
10. Number of Pull Requests 
11. Number of accepted Pull Requests
12. Number of Forks
13. Number of Branches
