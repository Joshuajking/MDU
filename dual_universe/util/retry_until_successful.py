def retry_until_success(function, max_attempts=4):
    attempts = 0
    while attempts < max_attempts:
        result = function()
        if result.request.status_code == 200:
            return result
        attempts += 1
    raise Exception("Maximum retry attempts reached.")
