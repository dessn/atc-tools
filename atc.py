#!/usr/bin/env python

import re

import atc_tools

def correct_service( service_name ) :
    if service_name == "user" :
        return "users"
    elif service_name == "observatory" :
        return "observatories"
    elif service_name == "field" :
        return "fields"
    elif service_name == "post" :
        return "posts"
    else :
        return service_name

def handle_create( args ) :
    service_name = correct_service( args.service )
    client       = atc_tools.default_client()
    service      = client.service( service_name )
    doc = vars( args )
    del doc[ "action"  ]
    del doc[ "service" ]
    del doc[ "func"    ]
    return service.post( doc )

def handle_get( args ) :
    service_name = correct_service( args.service )
    client       = atc_tools.default_client()
    service      = client.service( service_name )
    return service.get( args._id, args.include, args.exclude )

def handle_list( args ) :
    service_name = correct_service( args.service )
    client       = atc_tools.default_client()
    service      = client.service( service_name )
    data = service.list( args.skip, args.limit, args.order, args.include, args.exclude, args.count )
    if "count" in data :
        return data[ "count" ]
    else :
        return data[ "docs" ]

def handle_update( args ) :
    service_name = correct_service( args.service )
    client       = atc_tools.default_client()
    service      = client.service( service_name )
    doc = vars( args )
    del doc[ "action"  ]
    del doc[ "service" ]
    del doc[ "func"    ]
    _id = doc.pop( "_id" )
    if "id" in doc :
        doc[ "_id" ] = doc.pop( "id" )
    return service.put( _id, doc )

def handle_delete( args ) :
    service_name = correct_service( args.service )
    client       = atc_tools.default_client()
    service      = client.service( service_name )
    return service.delete( args._id )

if __name__ == "__main__" :

    import argparse
    import pprint

    # Top-level parser.

    parser     = argparse.ArgumentParser( description = "ATC command line interface" )
    subparsers = parser.add_subparsers( dest = "action" )

    create_parser = subparsers.add_parser( "create"                         , 
            description = "Create a new document."                          )

    get_parser = subparsers.add_parser( "get"                               , 
            description = "Get a single document."                          )

    list_parser = subparsers.add_parser( "list"                             , 
            description = "List multiple documents."                        )

    update_parser = subparsers.add_parser( "update"                         , 
            description = "Update a document."                              )

    delete_parser = subparsers.add_parser( "delete"                         , 
            description = "Delete a document."                              )

    # Handlers.

    create_parser.set_defaults( func = handle_create  )
    get_parser.set_defaults   ( func = handle_get     )
    list_parser.set_defaults  ( func = handle_list    )
    update_parser.set_defaults( func = handle_update  )
    delete_parser.set_defaults( func = handle_delete  )

    # Get command parser.

    get_parser.add_argument( "service"                                      , 
            help = "service hosting the document to retrieve"               )

    get_parser.add_argument( "_id"                                          , 
            help = "document identifier"                                    )

    get_parser.add_argument( "--include", "-i"                              , 
            help  = "specific fields to include [%(default)s]"              , 
            nargs = "+"                                                     )

    get_parser.add_argument( "--exclude", "-e"                              , 
            help  = "specific fields to exclude [%(default)s]"              , 
            nargs = "+"                                                     )

    # List command parser.

    list_parser.add_argument( "service"                                     , 
            help = "service hosting the documents to retreive"              )

    list_parser.add_argument( "--skip", "-s"                                , 
            help = "number of entries to skip [%(default)s]"                , 
            type = int                                                      )

    list_parser.add_argument( "--limit", "-l"                               ,
            help = "limit number of entries returned [%(default)s]"         , 
            type = int                                                      )

    list_parser.add_argument( "--order", "-o"                               , 
            help    = "sort order if any [%(default)s]"                     , 
            nargs   = "+"                                                   )

    list_parser.add_argument( "--include", "-i"                             , 
            help  = "specific fields to include [%(default)s]"              , 
            nargs = "+"                                                     )

    list_parser.add_argument( "--exclude", "-e"                             ,
            help  = "specific fields to exclude [%(default)s]"              , 
            nargs = "+"                                                     )

    list_parser.add_argument( "--count", "-c"                               , 
            help   = "return only count of matched documents [%(default)s]" , 
            action = "store_true"                                           )

    # Delete command parser.

    delete_parser.add_argument( "service"                                   , 
            help = "service hosting the document to delete"                 )

    delete_parser.add_argument( "_id"                                       , 
            help = "identifier of document to delete"                       )

    # For the sake of clarity, the create and update command parsers
    # are defined service by service.  Optional arguments that are not
    # supplied default values here will have some default determined 
    # by the server side.

    create_subparsers = create_parser.add_subparsers( dest = "service" )
    update_subparsers = update_parser.add_subparsers( dest = "service" )

    # Fields service create.

    create_field_parser = create_subparsers.add_parser( "field"             , 
            description = "Create and store a new field document."          )

    create_field_parser.add_argument( "_id"                                 , 
            help = "new field's ID"                                         )

    create_field_parser.add_argument( "ra"                                  , 
            help = "new field's center right ascension"                     )

    create_field_parser.add_argument( "dec"                                 , 
            help = "new field's center declination"                         )

    create_field_parser.add_argument( "ra_semiaxis"                         , 
            help = "new field's right ascension semiaxis in degrees"        ,
            type = float                                                    )

    create_field_parser.add_argument( "dec_semiaxis"                        , 
            help = "new field's declination semiaxis in degrees"            ,
            type = float                                                    )

    create_field_parser.add_argument( "--units"                             , 
            dest    = "__units__"                                           ,
            help    = "coordinate units"                                    , 
            default = "degrees"                                             ,
            choices = [ "degrees", "sexagesimal" ]                          )

    # Observatories service create.

    observatory_description = """Create and store a new observatory document.
    If only an _id value, or only _id and name values, are provided, then a
    matching SLALIB observatory record will be used to fill in the other
    values.  Note well the east-positive sign convention on longitude!"""

    create_observatory_parser = create_subparsers.add_parser( "observatory"    , 
            description = re.sub( "\s+", " ", observatory_description )        )

    create_observatory_parser.add_argument( "_id"                              , 
            help = "new observatory's ID"                                      )

    create_observatory_parser.add_argument( "--name"                           , 
            help    = "new observatory's name"                                 ,
            default = argparse.SUPPRESS                                        )

    create_observatory_parser.add_argument( "--longitude"                      , 
            help    = "new observatory's *east-positive* sexagesimal longitude",
            default = argparse.SUPPRESS                                        )

    create_observatory_parser.add_argument( "--latitude"                       , 
            help    = "new observatory's latitude sexagesimal longitude"       ,
            default = argparse.SUPPRESS                                        )

    create_observatory_parser.add_argument( "--altitude"                       , 
            help    = "new observatory's altitude in meters"                   ,
            default = argparse.SUPPRESS                                        , 
            type    = float                                                    )

    # Users service create.

    create_user_parser = create_subparsers.add_parser( "user"               , 
            description = "create and store a new user document"            )

    create_user_parser.add_argument( "_id"                                  , 
            help = "new user's ID"                                          )

    create_user_parser.add_argument( "name"                                 , 
            help = "new user's name"                                        )

    create_user_parser.add_argument( "email"                                , 
            help = "new user's email address"                               )

    create_user_parser.add_argument( "--label-color"                        , 
            help    = "user label background color"                         , 
            default = argparse.SUPPRESS                                     )

    create_user_parser.add_argument( "--administrator"                      , 
            help    = "grant administrator role to the new user"            , 
            default = argparse.SUPPRESS                                     , 
            action  = "store_true"                                          )

    create_user_parser.add_argument( "--inceptor"                           , 
            help    = "grant target inceptor role to the new user"          , 
            default = argparse.SUPPRESS                                     , 
            action  = "store_true"                                          )

    # Users service update.

    update_user_parser = update_subparsers.add_parser( "user"               , 
            description = "update an existing user document"                )

    update_user_parser.add_argument( "_id"                                  , 
            help = "identifier of user document to modify"                  )

    update_user_parser.add_argument( "--id"                                 , 
            help    = "replacement user ID"                                 ,
            default = argparse.SUPPRESS                                     )

    update_user_parser.add_argument( "--name"                               , 
            help    = "replacement user name"                               , 
            default = argparse.SUPPRESS                                     )

    update_user_parser.add_argument( "--email"                              , 
            help    = "replacement email address"                           , 
            default = argparse.SUPPRESS                                     )

    update_user_parser.add_argument( "--label-color"                        , 
            help    = "label background color"                              , 
            default = argparse.SUPPRESS                                     )

    update_user_parser.add_argument( "--grant-administrator"                , 
            help    = "grant administrator role to user"                    , 
            default = argparse.SUPPRESS                                     , 
            dest    = "administrator"                                       , 
            action  = "store_true"                                          )

    update_user_parser.add_argument( "--revoke-administrator"               , 
            help    = "revoke user's administrator role"                    , 
            default = argparse.SUPPRESS                                     , 
            dest    = "administrator"                                       , 
            action  = "store_false"                                         )

    update_user_parser.add_argument( "--grant-inceptor"                     , 
            help    = "grant target inceptor role to user"                  , 
            default = argparse.SUPPRESS                                     , 
            dest    = "inceptor"                                            , 
            action  = "store_true"                                          )

    update_user_parser.add_argument( "--revoke-inceptor"                    , 
            help    = "revoke user's target inceptor role"                  , 
            default = argparse.SUPPRESS                                     , 
            dest    = "inceptor"                                            ,
            action  = "store_false"                                         )

    # Parse arguments and print output.

    args = parser.parse_args()
    pprint.pprint( args.func( args ) )
