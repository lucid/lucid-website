from django.db import models

# Borrowed from the django snipplets app
# Adapted to use the 

class RatingsManager(models.Manager):
    """
    Custom manager for the Rating model.

    Adds shortcuts for fetching aggregate data on a given Version,
    lists of top-rated Snippets, and for quickly determining whether
    someone's already rated a given Version.
   
    """
    def already_rated(self, user_id, version_id):
        """
        Determines whether a User has already rated a given Version.
       
        """
        try:
            rating = self.get(user__pk=user_id, version__pk=version_id)
        except self.model.DoesNotExist:
            return False
        return True
   
    def ratings_for_version(self, version_id):
        """
        Returns all Ratings for a given Snippet.
       
        """
        return self.filter(snippet__pk=version_id)
   
    def score_for_version(self, version_id):
        """
        Returns the current rating score for a Snippet as a dictionary
        with the following keys:
       
            score
                The total score.
            num_ratings
                The number of ratings so far.
       
        """
        query = """SELECT AVG(score), COUNT(*)
        FROM %s
        WHERE version_id=%%s""" % self.model._meta.db_table
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [version_id])
        result = cursor.fetchall()[0]
        if result[0] == None:
            return { 'score': 0.0, 'num_ratings': 0 }
        return { 'score': result[0], 'num_ratings': result[1] }
   
    def top_rated(self, num=5):
        """
        Returns the top ``num`` Snippets with net positive ratings, in
        order of their total rating score.
       
        """
        from models import Version
        query = """SELECT version_id, AVG(score) * SUM(score) AS rating
        FROM %s
        GROUP BY version_id
        ORDER BY rating DESC""" % self.model._meta.db_table
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [])

        version_ids = [row[0] for row in cursor.fetchall()]
        version_dict = Version.objects.in_bulk(version_ids)
        return [version_dict[version_id] for version_id in version_ids][:num]
    
    def most_rated(self, num=5):
        """
        Returns the top ``num`` Snippets with net positive ratings, in
        order of their total rating score.
       
        """
        from models import Version
        query = """SELECT version_id, COUNT(score) AS rating
        FROM %s
        GROUP BY version_id
        ORDER BY rating DESC""" % self.model._meta.db_table
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query, [])

        version_ids = [row[0] for row in cursor.fetchall()]
        version_dict = Version.objects.in_bulk(version_ids)
        return [version_dict[version_id] for version_id in version_ids]


