import sys
import requests
import math
import re

from collections import defaultdict
from difflib import SequenceMatcher

def get_contacts(page, per_page):
    url = f'https://api.churchsuite.com/v1/addressbook/contacts?page={page}&per_page={per_page}'
    headers = {
        'X-Auth': 'REPLACE WITH CHURCHSUITE API KEY',
        'X-Application': 'integration',
        'X-Account': 'REPLACE WITH CHURCHSUITE ACCOUNT NAME'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} - {response.text} from the API. Exiting...")
        sys.exit(1)  # Exit the script with an error code

    return response.json()

def fetch_all_contacts():
    all_contacts = []
    page = 1
    per_page = 50

    while True:
        response = get_contacts(page, per_page)
        contacts = response['contacts']
        if not contacts:
            break

        all_contacts.extend(contacts)
        total_pages = math.ceil(
            response['pagination']['no_results'] / response['pagination']['per_page'])
        if page >= total_pages:
            break

        page += 1

    return all_contacts

def is_invalid_last_name(last_name):
    return not bool(re.match("^[a-zA-Z-' ]+$", last_name))

#  The similiarity ratio is set 0.85. This ratio determines when two names are considered similar. 
#  The value `0.85` means names with an 85% similarity will be flagged as similar.
#  If you find that too many or too few names are flagged as similar, you can adjust this threshold as required
def are_names_similar(name1, name2):
 similarityRatio = 0.85
 return SequenceMatcher(None, name1.lower(), name2.lower()).ratio() > similarityRatio

# Function to log contacts with email addresses to a CSV file 
def log_contacts_with_emails(contacts):
    with open("address_book-analysis.csv", "w") as log_file:
        log_file.write("First Name,Last Name,Email Address\n")  # Write header row
        for contact in contacts:
            if contact['email']:
                log_entry = f"{contact['first_name']},{contact['last_name']},{contact['email']}\n"
                log_file.write(log_entry)

def main():
    all_contacts = fetch_all_contacts()

    duplicate_phones = defaultdict(set)
    duplicate_emails = defaultdict(list)
    duplicate_names = defaultdict(list)
    invalid_last_names = []
    similar_names = []
    missing_phones = set()
    missing_emails = set()

    for i, current_contact in enumerate(all_contacts):
        current_name = f"{current_contact['first_name']} {current_contact['last_name']}"

        if is_invalid_last_name(current_contact['last_name']):
            invalid_last_names.append(current_contact)

        if not current_contact['telephone']:
            missing_phones.add(current_contact['id'])

        if not current_contact['email']:
            missing_emails.add(current_contact['id'])

        for comparison_contact in all_contacts[i + 1:]:
            if current_contact['id'] != comparison_contact['id']:

                comparison_name = f"{comparison_contact['first_name']} {comparison_contact['last_name']}"

                if current_contact['telephone'] and current_contact['telephone'].strip() == comparison_contact['telephone'].strip():
                    duplicate_phones[current_contact['telephone']].add(
                        current_contact['id'])
                    duplicate_phones[current_contact['telephone']].add(
                        comparison_contact['id'])

                if current_contact['email'] and current_contact['email'].lower() == comparison_contact['email'].lower():
                    duplicate_emails[current_contact['email']].extend(
                        [current_contact, comparison_contact])

                if current_name.lower() == comparison_name.lower():
                    duplicate_names[current_name].extend([current_contact, comparison_contact])

                if are_names_similar(current_name, comparison_name) and current_name.lower() != comparison_name.lower():
                    similar_names.append((current_contact, comparison_contact))

    print("Duplicate phone numbers:")
    for phone, contact_ids in duplicate_phones.items():
        print(f"  Phone number: {phone}")
        for contact_id in contact_ids:
            contact = next(
                c for c in all_contacts if c['id'] == contact_id)
            print(
                f"    {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")

    print("\n\nDuplicate emails:")
    for email, contacts in duplicate_emails.items():
        print(f"Email: {email}")
        for contact in contacts:
            print(
                f"  {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")

    print("\nDuplicate names:")
    for name, contacts in duplicate_names.items():
        print(f"Name: {name}")
        for contact in contacts:
            print(
                f"  {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")

    print("\nInvalid last names:")
    for contact in invalid_last_names:
        print(
            f"  {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")

    print("\nSimilar names:")
    for current_contact, comparison_contact in similar_names:
        print(f"  {current_contact['first_name']} { current_contact['last_name']} (ID: {current_contact['id']}) - {comparison_contact['first_name']} {comparison_contact['last_name']} (ID: {comparison_contact['id']})")

    print("\nMissing phone numbers:")
    for contact_id in missing_phones:
        contact = next(c for c in all_contacts if c['id'] == contact_id)
        print(f"  {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")

    print("\nMissing emails :")
    for contact_id in missing_emails:
        contact = next(c for c in all_contacts if c['id'] == contact_id)
        print(f"  {contact['first_name']} {contact['last_name']} (ID: {contact['id']})")

    log_contacts_with_emails(all_contacts)

if __name__ == "__main__":
    main()
