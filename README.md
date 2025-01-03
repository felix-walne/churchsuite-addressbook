### README for ChurchSuite Contacts Management Script

This Python script fetches address book contacts from the ChurchSuite API, processes the data to identify issues such as duplicates, invalid names, and missing information, and logs contacts with email addresses to a CSV file.

#### Features:
- **Fetch contacts**: Retrieves contacts using pagination from the ChurchSuite API.
- **Data validation**:
  - Identifies **invalid last names** (non-alphabetic).
  - Flags contacts with **missing phone numbers** or **emails**.
  - Detects **duplicate phone numbers**, **emails**, and **names**.
  - Checks for **similar names** using a similarity ratio.
- **CSV Logging**: Logs contacts with email addresses to `contacts_with_emails.csv`.
- **Displays results**: Prints duplicates, missing information, and issues.

#### Prerequisites:
1. **Python 3**: Install Python 3.x.
2. **Install Required Libraries**: This script requires several Python libraries for processing data and interacting with the ChurchSuite API. To install the necessary libraries, run the following command::
   ```bash
   pip install requests
   ```
3. **ChurchSuite API**: Replace the placeholders in the script for your API key and account name:
   ```python
   'X-Auth': 'REPLACE WITH CHURCHSUITE API KEY',
   'X-Account': 'REPLACE WITH CHURCHSUITE ACCOUNT NAME'
   ```

#### How to Use:
1. **Configure API details**: Replace API credentials in the script.
2. **Run the script**:
   ```bash
   python3 churchsuite_contacts.py
   ```
3. **View CSV**: A file `address_book-analysis.csv` will be created with contacts containing email addresses.

#### Name Similarity Comparison:
- The script uses a **similarity ratio** (default set to `0.85`) to compare names. This ratio determines when two names are considered similar. The value `0.85` means names with an 85% similarity will be flagged as similar.
- **Adjust the threshold**: If you find that too many or too few names are flagged as similar, you can adjust this threshold by modifying the value `0.85` in the `are_names_similar()` function:
   ```python
   def are_names_similar(name1, name2):
       return SequenceMatcher(None, name1.lower(), name2.lower()).ratio() > 0.85
   ```
   For example, setting the value to `0.90` would require a 90% similarity for names to be flagged as similar, reducing false positives.


#### Troubleshooting:
- **API Errors**: Ensure the API key and account name are correct.