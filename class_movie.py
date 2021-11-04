

class Movie(object):
    
    def __init__(self, movie_id , title, date_added, on_hold, viewed):
        self.movie_id = movie_id
        self.title = title
        self.dateadded = date_added
        self.on_hold = on_hold
        self.viewed = viewed
#        self.delflag = delflag # only a database field, not necessary for class?

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def on_hold(self):
        return self._on_hold

    @on_hold.setter
    def on_hold(self, value):
        self._on_hold = value

    @property
    def viewed(self):
        return self._viewed

    @viewed.setter
    def viewed(self, value):
        self._viewed = value

    def __str__(self):
        # returns a human readable version of the object. Often called when {object}.str() is used
        return "Movie(id: {}, title: {}, date added: {}, on hold: {}, viewed: {})".format(self.movie_id, self.title, self.dateadded, self.on_hold, self._viewed)



result = Movie(1,"Snatch", "2021-10-29", "0", "1")
# result.viewed()
print(result.viewed)

class Result(object):
    
    def __init__(self, result_title, format, pubdate, rating, url):
        self.result_title = result_title
        self.format = format
        self.pubdate = pubdate
        self.rating = rating # tuple? list?
        self.url = url



# class Employee:

#     def __init__(self, first, last, pay):
#         self.first = first
#         self.last = last
#         self.pay = pay

#     @property
#     def email(self):
#         return '{}.{}@email.com'.format(self.first, self.last)

#     @property
#     def fullname(self):
#         return '{} {}'.format(self.first, self.last)

#     def __repr__(self):
#         return "Employee('{}', '{}', '{}')".format(self.first, self.last, self.pay)