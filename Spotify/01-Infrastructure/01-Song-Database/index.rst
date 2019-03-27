Song Database
==============================================================================


What is Song Database
------------------------------------------------------------------------------

The most important concept in a music app is a song. And everything else connects to song directly or indirectly. For example:

- an ``Album`` is a collection of songs.
- an ``Artist`` is the author of a collection of songs; Each song is associated with at least on Artist (Unknown Artist is also an artist).
- a ``Playlist`` is also a collection of songs.
- a ``User`` listens songs.
- a ``Queue`` is a list of songs been played by a user in time order.
- etc ...

So the song database is extremely important in our business.


Choose the Database
------------------------------------------------------------------------------

**User Behavior Analysis**:

what a user could do on Spotify App?

1. Search a song, by title, artist, ...
2. Search artist, album, playlist by ...
3. Find out songs and album published by an artist ...
4. Create their own playlist, and manage it.
5. Like a song, save album, follow an artist, subscribe a playlist, ...
6. Randomly browse songs by genre, artist, other user TOP x billboard list.
7. Ask Spotify to recommend songs by song, playlist, album, artist, genre ...

**Query Pattern: real time query**

- My Library Page: list all saved songs
- My Library Page: list all saved albums
- My Library Page: list followed artists
- My Library Page: list saved playlist
- My Library Page: list recent listening queue
- Go Album: list all songs in the album
- Go Artist: list all songs / album created by the artist

**Query Pattern: non real time query**

- Monthly listeners for an Artist
- Total listened for a song
- Number of follower for an Artist
- Number of subscription for a list

**Scale of the database**:

- Songs: 35 M
- Paid Users: 83 M
- Monthly Active User: 180 M
- Total Users: let's say, 1000 M

Data Volume - Song:

In average, each song, 4 minutes, 320KBPS, 2.4MB / Minute, plus lyrics, metadata, is 10MB. In total, we need 35M * 10MB = 350TB Data Storage

Data Volume - User Generated Data:

In average, 1 MB for stateful data per users, 10 MB for behavior data per users.

In database, we usually only store the stateful data, and the most recent one month of behavior data history. Other history data goes to OLAP storage. 1000 M * 1MB = 1000TB Data Storage


**Our final decision**:

As far as I know, **Spotify use Cassandra**. Because of the visit pattern usually returns limited songs. Cassandra provide high performance read / write on primary key. Which suit the use case very well.

BUT, to challenge my self, I want to implement the database with MongoDB, another scalable, high performance, non-sql database.


Table (Collection in MongoDB) Design
------------------------------------------------------------------------------

**Entities**:

- Song
- User
- Artist
- Album
- Playlist

**Relationship**:

- Song to Album: Many to One, a song may be included in multiple album, but it is not a common case, and the cover image for different album usually different. So we don't mind to save the binary multiple times with different metadata.
- Song to Playlist: Many to Many
- Song to Artist: Many to Many
- Artist to Album: Many to Many

- User to Artist: Many to Many
- User to Album: Many to Many
- User to Playlist: Many to Many

Looks like we have a lots of Many to Many.

**Design for Many to Many**:

In Relational Database, we usually use association table for this. But we are not using Relational Database here.

In Non-SQL, we usually have 3 solution for many to many relationship. Let's take Song to Playlist as an example:

1. One side nest: Store information in Song
2. One side nest: Store information in Playlist
3. Both side nest: Store information in Both

One side nest in Playlist:

Data:

.. code-block:: python

    # song
    [
        {
            "song_id": 1,
            ...
        },
    ]

    # playlist
    [
        {
            "playlist_id": 1,
            "songs": [1, 2, 3, ...],
            ...
        }
    ]

Query:

.. code-block:: python

    # list songs in playlist, fast
    for song_id in playlist.find_by_id(1)["songs"]:
        song = song.find_by_id(song_id)
        ...

    # list playlist that include this song, slower
    for plist in playlist.find({"songs": 1}):
        ...

But 99% use case is to list songs in a playlist, and we want it to be fast.

In two side nest, query on both side is fast and convenient. But it is little bit hard to update both atomically, because when you add / remove a song to a playlist, you need to modify both collection. And it is two action in MongoDB.

In conclusion, in most cases, query from one side is way more common than the other, so we use one side nest for many-to-many relationship.

- Song to Playlist: Many to Many, nest song in playlist
    - list songs in a playlist
    - list playlist includes this song
- Song to Artist: Many to Many, use two way nest, and store artist name as redundancy in song
    - list songs published by an artist
    - list artists for this song
- User to Artist: Many to Many, nest artist in user
    - list artists you subscribed
    - count how many users subscribed this artist
- User to Album: Many to Many, nest album in user
    - list album you saved
    - count how many users saved this album
- User to Playlist: Many to Many, nest playlist in user
    - list playlist you created
    - count how many users subscribe this playlist


About the Audio Binary
------------------------------------------------------------------------------

Music content size varies from KB to over 100MB for long length audio. It should not stored with metadata in the database. We should use a separate music content streaming server for this purpose. The Audio Binary Entity ID should not associated with song id, because one song may be included in different album with different cover image.
