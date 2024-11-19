# within urls.py
from .views import csrf_token
urlpatterns = [
    path('api/csrf-token/', csrf_token),
]


# create new views.py file with the following:
from django.http import JsonResponse
from django.middleware.csrf import get_token

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


# within settings.py 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]

# Potential addition to settings.py
# this adds CORS which allows same-site trusted ports
# Cross-Origin Resource Sharing
INSTALLED_APPS = [
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



# create new csrf.js file
# this will fetch the CSRF token to the front end and store it in a component state 
import { useState, useEffect } from 'react';

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
};


# any file with a POST request
# this hook on a button that makes a POST Request
import { useCsrfToken } from './csrf';

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
}