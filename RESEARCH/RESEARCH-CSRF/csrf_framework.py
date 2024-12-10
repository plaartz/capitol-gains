# within urls.py
""" from .views import csrf_token
urlpatterns = [
    path('api/csrf-token/', csrf_token),
] """


# create new views.py file with the following:
""" from django.http import JsonResponse
from django.middleware.csrf import get_token

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

 """
# within settings.py 
""" REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
] """

# Potential addition to settings.py
# this adds CORS which allows same-site trusted ports
# Cross-Origin Resource Sharing
""" INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# allows cookies for CSRF
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:48003',
]

# Allow your React app's origin
CORS_ALLOWED_ORIGINS = [
    'http://localhost:PORT',
]
 """


# create new csrf.js file
# this will fetch the CSRF token to the front end and store it in a component state 
""" import { useState, useEffect } from 'react';

export const useCsrfToken = () => {
    const [csrfToken, setCsrfToken] = useState('');

    useEffect(() => {
        const fetchCsrfToken = async () => {
            const response = await fetch('/api/csrf-token/', {
                credentials: 'include' // Ensures cookies are included
            });
            const data = await response.json();
            setCsrfToken(data.csrfToken);
        };
        fetchCsrfToken();
    }, []);

    return csrfToken;
}; """


# any file with a POST request
# this hook on a button that makes a POST Request
""" import { useCsrfToken } from './csrf';

function YourComponent() {
    const csrfToken = useCsrfToken();

    const handlePostRequest = async () => {
        const response = await fetch('/your/api/endpoint/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ /* your data here */ }),
            credentials: 'include', // Allows cookies to be sent with the request
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
        } else {
            console.error("Failed to submit data");
        }
    };

    return (
        <button onClick={handlePostRequest}>Submit</button>
    );
} """

#above is what I found with some research, what could work within the project.

#below is what can be used using Django's built-in CSRF protection, copy/pasted from sources given by TA 

#A drop-in React component for submitting forms with a Django CSRF middleware token.
""" import React from 'react';
import DjangoCSRFToken from 'django-react-csrftoken'

class MyLoginForm extends React.Component {
  render(){
    return (
      <div className="container">
          <form>
            <DjangoCSRFToken/>
            // email
            // password
            // submit button
          </form>
      </div>
    )
  }
} """

""" from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def register_view(request):
    # // ... """


#csrf token within docs
""" function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} """

#Now, you can retrieve the CSRF token by calling the getCookie('csrftoken') function
""" var csrftoken = getCookie('csrftoken'); """


#Next you can use this csrf token when sending a request with fetch() by assigning the retrieved token to the X-CSRFToken header.
"""  fetch(url, {
    credentials: 'include',
    method: 'POST',
    mode: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: {}
   })
  } """

# If you are using React to render forms instead of Django templates you also need to render the csrf token because the Django tag { % csrf_token % } 
# is not available at the client side so you need to create a higher order component that retrieves the token using the getCookie() function and render
# it in any form.

#Lets add some line in csrftoken.js file.
""" import React from 'react';

var csrftoken = getCookie('csrftoken');

const CSRFToken = () => {
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
};
export default CSRFToken; """

# Then you can simply import it and call it inside your form
""" import React, { Component , PropTypes} from 'react';

import CSRFToken from './csrftoken';


class aForm extends Component {
    render() {

        return (
                 <form action="/endpoint" method="post">
                        <CSRFToken />
                        <button type="submit">Send</button>
                 </form>
        );
    }
}

export default aForm; """

# React renders components dynamically that's why Django might not be able to set a CSRF token cookie if you are rendering your form with React
# To solve this issue Django provides the ensurecsrfcookie decorator that you need to add to your view function

""" from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def myview(request): """