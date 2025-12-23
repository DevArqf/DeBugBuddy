def validate_error_input(error_input):
    if not error_inpu.strip():
        raise ValueError('Error input cannot be empty')