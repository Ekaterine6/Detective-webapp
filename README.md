# Detective board/news/case investigation web application

[Video demo on youtube] (https://youtu.be/un5Q4oKmTyc)

# Overview:

**This web application is a platform for organizing investigations, cases and evidence in a interactive workspace,** user are able to create news and cases, add those news to said cases as „evidence“ to further prove their point/case. They can write theories/ideas... in these cases and either make these cases public or private, if private of course only they can see the information in their cases, but if public then other users are able to see these cases and even interact with it to provide more information to the author about the said case or just give their opinion on things,  by commenting or replying to each others comments. The detective board lets the users brainstorm by creating/taking notes and displaying them as they please on the board. Each user has their own profile that displays their name, bio, join date, cases and posts created by them.

This application uses both python and django for the backend, and javascript on the frontend handling most of the interactivity. The application is mobile responsive except for one function - dragging the notes in the board page, other than that everything is mobile responsive. 


# Design:

The design and visuals are all inspired by this dark/mysterious „hacker“ theme that we see in movies and documentaries. I wanted the user to feel like they were going undercover and discovering something hidden or like a detective solving cases. Of course this design is fully fictional and for the users entertainment, no real hacking functionality.


# Distinctiveness and Complexity:

This project definitely draws upon the course’s lessons but it is distinct from other CS50w projects because it is not a social network like project 4 where users follow, like, or communicate/text each other. It does let the user post news but this is not the main goal of the web app, it is used to gain information and build cases on that information from the post or just to add to an existing case as evidence. When the case is public the users are allowed to comment but again there is no feed system such as liking comments or anything of that sort. my goal for letting the users comment is to let them share more information on the cases to let the author know more. 
This project is also not anywere near an ecommerce like project 2. I tried to emphasize on research, note taking, brainstorming and sharing news. The project also has a fully configured django admin panel, all core models are registered, so the admin can control posts, cases, users, images and comments.

When it comes to complexity, i did use lot of django models (specificaly 7) to manage profiles, posts, images(multiple, the users are able to share lot of „evidence“ pictures in their posts) , Cases, CaseEvidence (letting the user add  news/posts to cases) , Comments, Notes (to display on the board) .  The views.py handle the registration, login, posts, create posts/create cases(forms), profiles, case details/view case( the information is limited but the users are able to press read more and they will see the whole case and post info.), add to case(adding the “evidence”/posts to cases), profile, board (saving the last position the notes were left by the user and creating notes and displaying them) and lastly delete note, I call a lot of these in javascript in my html templates. The search bar allows the user to search for all the posts in the app by typing any information from the post (city , country, tags, text, title).



# File contents:

## Views.py / models.py / admin.py – already described above;
## Urls.py – paths/routes to views;
## Templates – html templates: add_to_case.html, create_case.html, layout.html, register.html, board.html, create_post.html, login.html, view_post.html, case_details.html, index.html, profile.html;
## Static – styles.css; 
## Media/ - post images, some pictures I used as example and user uploaded pictures are saved here;
## Requirments.txt – lists required python packages (Django==4.2.7    pillow==12.0.0);


# How to run the application:

1. main directory no need to cd into any other directory
2. create venv - run:  python -m venv venv 
3. activate venv : source venv/bin/activate
4. install requirements
5. make migration : python manage.py makemigrations 
6. migrate : python manage.py migrate
7. run: python manage.py runserver
8. To access admin run : python manage.py createsuperuser	


# additional information

- when a user first registerest and they open the board they will see an example note that is shown only once and after deleted it won't show again.

- notes can be given a color depending on what the user chosses (clue, idea, suspect) to further help them brainstorm and feel like a detective,


