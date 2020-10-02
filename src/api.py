import os
import requests

API_URL = os.getenv('ANINFO_API_URL')


def get_media_by_name(name, type=None):
    '''
        Get Manga or Anime by name
    '''

    query = '''
        query($name: String, $type: MediaType){
            Media (search: $name, type: $type) {
                id
                title {
                    romaji
                    english
                    native
                }
                format
                status
                description(asHtml: true)
                startDate{
                    day
                    month
                    year
                }
                endDate {
                    day
                    month
                    year
                }
                episodes
                chapters
                volumes
                duration
                bannerImage
                genres
                averageScore
                popularity
                favourites
                isAdult
                studios{
                    nodes{
                        name
                    }
                }
            }
        }
    '''

    variables = {
        'name' : name,
        'type': type
    }

    req = requests.post(API_URL, json={'query':query, 'variables': variables })

    return req.json()


def get_media_by_id(id, type=None):
    '''
        Get Anime or Manga by Id
    '''

    query = '''
        query($id: Int, $type: MediaType){
            Media (id: $id, type: $type) {
                id
                title {
                    romaji
                    english
                    native
                }
                format
                status                                                                description(asHtml: true)
                startDate{
                    day
                    month
                    year
                }
                endDate {
                    day
                    month
                    year
                }
                episodes
                chapters
                volumes
                duration
                bannerImage
                genres
                averageScore
                popularity
                favourites
                isAdult
                studios{
                    nodes{
                        name
                    }
                }
            }
        }
    '''

    variables = {
        "id":id,
        "type":type
    }

    res = requests.post(API_URL, json={'query':query, 'variables':variables})

    return res.json()


def get_character_by_name(name):
    '''
        Get Character Info by Name
    '''
    query = '''
        query($name: String){
            Character(search: $name){
                id
                name {
                    first
                    last
                    full
                    native
                }
                image {
                    medium
                }
                description(asHtml: true)
                favourites
                media {
                    nodes {
                        title {
                            english
                        }
                    }
                }
            }
        }

    '''

    variables = {
        'name':name
    }

    req = requests.post(API_URL, json={'query': query, 'variables':variables})

    return req.json()

def get_character_by_id(id):
    '''
        Get Character Info by Id
    '''
    query = '''
        query($id: Int){
            Character(id: $id){
                id
                name {
                    first
                    last
                    full
                    native
                }
                image {
                    medium
                }
                description(asHtml: true)
                favourites
                media {
                    nodes {
                        title {
                            english
                        }
                    }
                }
            }
        }

    '''

    variables = {
        'id':id
    }

    req = requests.post(API_URL, json={'query': query, 'variables':variables})

    return req.json()

def get_studio_by_name(name):
    '''
        Get Studio by Name
    '''

    query = '''
        query ($name: String){
            Studio(search: $name){
                id
                name
                media {
                    nodes {
                        title {
                            english
                        }
                    }
                }
                favourites
            }
        }
    '''

    variables = {
        'name' : name
    }

    req = requests.post(API_URL, json={'query':query, 'variables':variables})

    return req.json()


def get_studio_by_id(id):
    '''
        Get Studio by Id
    '''

    query = '''
        query ($id: Int){
            Studio(id: $id){
                id
                name
                media {
                    nodes {
                        title {
                            english
                        }
                    }
                }
                favourites
            }
        }
    '''

    variables = {
        'id' : id
    }

    req = requests.post(API_URL, json={'query':query, 'variables':variables})

    return req.json()



print(get_studio_by_id(1))
