def get_custom_css():
    return """
    <style>
    div[data-baseweb="select"] > div {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
    }
    </style>
    """
