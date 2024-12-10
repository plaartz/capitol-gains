# Research Report
## CSRF Token Protection and How it Works
### Summary of Work
The research being done for this part of the project was learning about what CSRF Protection is, and how we need to implement this with our project. I watched YouTube videos, went online into tutorials and websites, and also asked ChatGPT certain questions to better understand how to complement this with our project.

### Motivation
It was agreed upon that CSRF was important to learn about because we could not do POST methods in Django without specifying '*#csrf exempt*' within any file that had a **POST** method. Therefore in order to learn why, and to be able to simulate a production version of our application with the idea that real-world customers could be using this app, we wanted to implement safety measures in different aspects of our code. Whether it was safety checks in direct inputs, indirect inputs, and any step in-between, being consistent was key and therefore we decided to look into CSRF Protection. 
### Time Spent
1. YouTube tutorials: 1 hour
2. Online forums: 2 hours
3. ChatGPT: 30 minutes
4. Development of Potential Steps: 2 hours

### Results
Here I will explain what I learned. I learned that CSRF stands for **Cross-Site Request Forgery**. It refers to a type of attack that can happen when an attacker gets between a user making a request to a web application, and making a request that was *forged* from a different link, and ultimately a harmful consequence.[^3] A common example is during Session Authentification when a user wishes to create an account for some application, and later decides to update their account. A CSRF attack would be able to get in-between the update command and forge a different command, like delete, and execute that command alongside the request.[^5] 

It ultimately does this with cookies, which are stored in your browser, so that every time you make a request, to LOGIN for example, the web application can verify your login. These cookies are sent *automatically* to the website, regardless of your domain. This is what is exploited from the attack: using your browser's cookies, which are automatically sent to the web application, to send a harmful POST request from an original request that was not intended to do so. The video example showed this type of scenario: The browser which saves your login request cookies can also be seen when accessing a random link from within the web application. This link has nothing to do with your user login info, but is still making the browser send cookies to the webn application anyway. Through these cookies, a user could *forge* a request to delete your account and the user would be out of luck.[^3]

I learned that there are "safe" and "unsafe" HTTP operations. Some "safe" operations include: **GET**, **HEAD**, and **OPTIONS**. Some "unsafe" operations include: **POST**, **PUT**, **PATCH**, and **DELETE**.[^4]

So, how does one protect against CSRF attacks? One can use randomized CSRF Tokens that are explicitly verified with each request. They are session-specific and are used in conjuction with unsafe methods. I also learned that Django has a built-in CSRF protection, and can be used for POST methods. [^1] [^2]

I reached out to the TA Mya and was able directed to some useful websites with utilized Django's built-in CSRF protection. It showed a manual way to use CSRF Tokens in forms in React, and how to render them properly [^6] [^7]

In the end, it was decided that our project did not need CSRF protection, and we did not implement it into the project.

### Sources
- DjangoProject[^1]
- DjangoProjectSettings[^2]
- Youtube: Cross-Site Forgery Request (CSRF) Explained[^3]
- Working with AJAX, CSRF, & CORS[^4]
- Django & React Session Authentication and CSRF | Part 3 - Sign Up and User Profile [^5]
- Drop-in React Component for Django CSRF Token [^6]
- StackOverflow: Manual CSRF Token + RESTful API [^7]

[^1]: https://docs.djangoproject.com/en/5.1/howto/csrf/#using-csrf-protection-with-ajax
[^2]: https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-CSRF_COOKIE_DOMAIN
[^3]: (https://www.youtube.com/watch?v=eWEgUcHPle0)
[^4]: https://www.django-rest-framework.org/topics/ajax-csrf-cors/
[^5]: https://www.youtube.com/watch?v=NFHiT4ncPD8
[^6]: https://github.com/iMerica/django-react-csrftoken/blob/master/README.md
[^7]: https://stackoverflow.com/questions/50732815/how-to-use-csrf-token-in-django-restful-api-and-react