#adapted from snapboard

import os

from django.db.models import signals 
from django.conf import settings

import models as repo_app

def sync_hook(**kwargs): 
    pass

signals.post_syncdb.connect(sync_hook, sender=repo_app) 




def test_setup(**kwargs):
    from django.contrib.auth.models import User
    from random import choice
    from desktopsite.apps.snapboard import chomsky
    from desktopsite.apps.repository.categories import REPOSITORY_CATEGORIES
    from models import Package, Rating, Version
    import datetime
    if not settings.DEBUG:
        return 

    if Package.objects.all().count() > 0:
        # return, since there seem to already be threads in the database.
        return
    
    # ask for permission to create the test
    msg = """
    You've installed Repository with DEBUG=True, do you want to populate
    the board with random users/packages/ratings to test-drive the application?
    (yes/no):
    """
    populate = raw_input(msg).strip()
    while not (populate == "yes" or populate == "no"):
        populate = raw_input("\nPlease type 'yes' or 'no': ").strip()
    if populate == "no":
        return

    # create 10 random users

    users = ('john', 'sally', 'susan', 'amanda', 'bob', 'tully', 'fran'
             'rick', 'alice', 'mary', 'steve', 'chris', 'becca', 'rob'
             'peter', 'amy', 'bill', 'nick', 'dustin', 'alex', 'jesus')
    for u in users:
        user, created = User.objects.get_or_create(username=u)
        user.email = "%s@%s.com" % (u, u)
        user.set_password(u)
        user.save()
        # user.is_staff = True

    # create up to 30 posts
    tc = range(1, 20)
    words = chomsky.objects.split(' ')
    for i in range(0, 20):
        print 'package ', i, 'created'
        subj = words[i]+" "+words[i-4]+" "+words[i+2]
        package = Package(
                        name=subj,
                        sysname=subj.replace(" ", "_").replace(".", "").replace("(", "").replace(")", ""),
                        category=choice(REPOSITORY_CATEGORIES)[0],
                        description = '\n\n'.join([chomsky.chomsky() for x in range(0, choice(range(2, 5)))]),
                        maintainer=choice(User.objects.all()),
                        url="http://www.foo.com/",
                       )
        package.save()
        
        for j in range(0, choice(range(1, 10))):
            text = '\n\n'.join([chomsky.chomsky() for x in range(0, choice(range(2, 5)))])
            v=Version(
              name="%s.%s.%s" % (choice(range(1, 5)), choice(range(1, 50)), choice(range(1, 170))),
              package=package,
              changelog=text,
              package_url="http://www.foo.com/bar.lucid.zip",
              checksum= "".join([choice("abcdef0123456789") for x in range(1, 50)]),
              verified_safe=choice((True, False)),
            )
            v.save()
            
            for adf in range(0, choice(tc)):
                rating = Rating(
                              user=User.objects.get(pk=adf+1),
                              version= v,
                              score=choice((1,2,3,4,5)),
                )
                rating.save()

signals.post_syncdb.connect(test_setup, sender=repo_app) 
# vim: ai ts=4 sts=4 et sw=4
