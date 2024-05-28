Issue Title: Improve Error Handling in fetchProcessCollection.py and __main__.py
Description:

The current implementation lacks robust error handling in fetchProcessCollection.py and __main__.py, which can lead to uninformative failures. Enhancing error handling will improve the application's robustness and maintainability.

Requirements:
Improve Error Handling in get_user_collection Function:
Use logging to record detailed error messages instead of print statements.
Ensure exceptions are appropriately propagated for proper handling by the calling function.
Enhance JSON File Handling in __main__.py:
Implement try-except blocks around JSON file operations to catch and handle exceptions like FileNotFoundError and JSONDecodeError.
Log meaningful error messages and provide fallback mechanisms or user-friendly messages.
Configure Consistent Logging:
Set up a consistent logging mechanism using Python's logging module.
Replace all print statements with appropriate logging calls.
Testing:
Write unit tests to cover the new error handling logic.
Validate that the application behaves correctly under various failure scenarios.