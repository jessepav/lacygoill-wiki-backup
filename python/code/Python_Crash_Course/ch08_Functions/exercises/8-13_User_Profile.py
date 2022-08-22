# Purpose: Start with a copy of `user_profile` from this chapter course.
# Build a profile of someone you  know by calling `build_profile()`, using their
# first and last names and three other key-value pairs that describe them.

# Reference: page 150 (paper) / 188 (ebook)

def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('pedro', 'pascal',
                             age=47,
                             location='new york',
                             occupation='actor')

print(user_profile)
#     {'age': 47, 'location': 'new york', 'occupation': 'actor', 'first_name': 'pedro', 'last_name': 'pascal'}
