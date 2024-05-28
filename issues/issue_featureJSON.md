Title: Implement JSON Saving for User Music Collection Data

Description:

Currently, our repository can authenticate and fetch user data from a music collection API but lacks the functionality to save this data. We need to add a feature to serialize and save the fetched music collection data into a JSON file. This will allow offline access and facilitate future data processing features.

Requirements:

Serialize API data into JSON after fetching.
Save JSON in a user-specified directory, avoiding overwrites by using timestamps in filenames.
Handle errors during file saving (e.g., permission issues, disk space).
Ensure compatibility with existing API authentication.
Include unit tests to verify the integration with existing data fetching.