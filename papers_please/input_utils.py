"""
Methods for input data handling.
"""


def user_input(msg, default=None, value_callback=None,
               trim_spaces=True, show_default=True, required=False):
    """Handle user input in string format."""
    if show_default and default is not None:
        msg += f' [{default}]'
    if default is not None:
        required = False

    while 1:
        value = input(f'{msg}: ')
        if trim_spaces:
            value = value.strip()

        if value:
            if value_callback is None:
                return value
            try:
                return value_callback(value)
            except ValueError:
                print('Your input is invalid, try again')
        else:
            if not required:
                return default
            print('You must enter something')


def input_int(msg, default=None, show_default=True, required=False):
    """Handle user input in integer format."""
    return user_input(
        msg, default, value_callback=int,
        show_default=show_default, required=required
    )


def confirm(msg,
            default_yes=False, default_no=False, required=False):
    """Handle user input in boolean format."""
    if default_yes and default_no:
        raise RuntimeError(
            'Both "default_yes" and "default_no" are "True".')

    def callback(value):
        """Redirect yes/no format to boolean."""
        answers = {
            'y': True,
            'yes': True,
            'n': False,
            'no': False
        }
        answer = answers.get(value.lower())

        if answer is None:
            valid_values = '/'.join(answers.keys())
            raise ValueError(f'Valid values: {valid_values}')

        return answer

    if default_yes:
        default = True
        msg += ' [Y/n]'
    elif default_no:
        default = False
        msg += ' [y/N]'
    else:
        default = None
        msg += ' [y/n]'

    return user_input(msg, default, value_callback=callback,
                      show_default=False, required=required)
