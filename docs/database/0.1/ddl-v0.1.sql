-- we don't know how to generate schema public (class Schema) :(
create table if not exists django_migrations
(
    id      serial       not null
    constraint django_migrations_pkey
    primary key,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied timestamp with time zone not null
);

create table if not exists users
(
    password       varchar(128) not null,
    last_login     timestamp with time zone,
    uuid           uuid not null
    constraint users_pkey
    primary key,
    email          varchar(254) not null
    constraint users_email_key
    unique,
    username       varchar(8)   not null
    constraint users_username_key
    unique,
    date_joined    timestamp with time zone not null,
    last_logged_in timestamp with time zone not null,
    is_active      boolean      not null,
    is_admin       boolean      not null
);

create index if not exists users_email_0ea73cca_like
on users (email);

create index if not exists users_username_e8658fc8_like
on users (username);

create table if not exists django_content_type
(
    id        serial       not null
    constraint django_content_type_pkey
    primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
    unique (app_label, model)
);

create table if not exists django_admin_log
(
    id              serial       not null
    constraint django_admin_log_pkey
    primary key,
    action_time     timestamp with time zone not null,
    object_id       text,
    object_repr     varchar(200) not null,
    action_flag     smallint     not null
    constraint django_admin_log_action_flag_check
    check (action_flag >= 0),
    change_message  text         not null,
    content_type_id integer
    constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
    references django_content_type
    deferrable initially deferred,
    user_id         uuid not null
    constraint django_admin_log_user_id_c564eba6_fk_users_uuid
    references users
    deferrable initially deferred
);

create index if not exists django_admin_log_content_type_id_c4bce8eb
on django_admin_log (content_type_id);

create index if not exists django_admin_log_user_id_c564eba6
on django_admin_log (user_id);

create table if not exists auth_permission
(
    id              serial       not null
    constraint auth_permission_pkey
    primary key,
    name            varchar(255) not null,
    content_type_id integer      not null
    constraint auth_permission_content_type_id_2f476e4b_fk_django_co
    references django_content_type
    deferrable initially deferred,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
    unique (content_type_id, codename)
);

create index if not exists auth_permission_content_type_id_2f476e4b
on auth_permission (content_type_id);

create table if not exists auth_group
(
    id   serial      not null
    constraint auth_group_pkey
    primary key,
    name varchar(80) not null
    constraint auth_group_name_key
    unique
);

create index if not exists auth_group_name_a6ea08ec_like
on auth_group ( name );

create table if not exists auth_group_permissions
(
    id            serial  not null
    constraint auth_group_permissions_pkey
    primary key,
    group_id      integer not null
    constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
    references auth_group
    deferrable initially deferred,
    permission_id integer not null
    constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
    references auth_permission
    deferrable initially deferred,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
    unique (group_id, permission_id)
);

create index if not exists auth_group_permissions_group_id_b120cbf9
on auth_group_permissions (group_id);

create index if not exists auth_group_permissions_permission_id_84c5c92e
on auth_group_permissions (permission_id);

create table if not exists authtoken_token
(
    key varchar(40)              not null
    constraint authtoken_token_pkey
    primary key,
    created timestamp with time zone not null,
    user_id uuid not null
    constraint authtoken_token_user_id_key
    unique
    constraint authtoken_token_user_id_35299eff_fk_users_uuid
    references users
    deferrable initially deferred
);

create index if not exists authtoken_token_key_10f0b77e_like
on authtoken_token ( key );

create table if not exists profiles
(
    uuid                      uuid not null
    constraint profiles_pkey
    primary key,
    profile_picture           varchar(100),
    is_receiving_notification boolean not null,
    profile_of_user_id        uuid not null
    constraint profiles_profile_of_user_id_5c60b466_fk_users_uuid
    references users
    deferrable initially deferred
);

create index if not exists profiles_profile_of_user_id_5c60b466
on profiles (profile_of_user_id);

create table if not exists parties
(
    id              serial      not null
    constraint parties_pkey
    primary key,
    title           varchar(25) not null,
    place           varchar(25) not null,
    description     text,
    start_time      timestamp with time zone not null,
    current_people  smallint    not null
    constraint parties_current_people_check
    check (current_people >= 0),
    max_people      smallint    not null
    constraint parties_max_people_check
    check (max_people >= 0),
    created_at      timestamp with time zone not null,
    last_updated    timestamp with time zone not null,
    is_new          boolean     not null,
    will_start_soon boolean     not null,
    has_started     boolean     not null,
    can_join        boolean     not null,
    party_owner_id  uuid not null
    constraint parties_party_owner_id_321d918c_fk_profiles_uuid
    references profiles
    deferrable initially deferred
);

create index if not exists parties_party_owner_id_321d918c
on parties (party_owner_id);

create table if not exists comments
(
    id           serial       not null
    constraint comments_pkey
    primary key,
    text         varchar(150) not null,
    created_at   timestamp with time zone not null,
    last_updated timestamp with time zone not null,
    is_active    boolean      not null,
    author_id    uuid not null
    constraint comments_author_id_7a23bb5d_fk_profiles_uuid
    references profiles
    deferrable initially deferred,
    party_id     integer      not null
    constraint comments_party_id_aaae0eeb_fk_parties_id
    references parties
    deferrable initially deferred
);

create index if not exists comments_author_id_7a23bb5d
on comments (author_id);

create index if not exists comments_party_id_aaae0eeb
on comments (party_id);

create table if not exists complains
(
    id         serial not null
    constraint complains_pkey
    primary key,
    text       text   not null,
    created_at timestamp with time zone not null,
    author_id  uuid not null
    constraint complains_author_id_b51bca81_fk_profiles_uuid
    references profiles
    deferrable initially deferred
);

create index if not exists complains_author_id_b51bca81
on complains (author_id);

create table if not exists notifications
(
    id         serial       not null
    constraint notifications_pkey
    primary key,
    text       varchar(100) not null,
    is_read    boolean      not null,
    created_at timestamp with time zone not null,
    user_id    uuid not null
    constraint notifications_user_id_468e288d_fk_profiles_uuid
    references profiles
    deferrable initially deferred
);

create index if not exists notifications_user_id_468e288d
on notifications (user_id);

create table if not exists django_session
(
    session_key  varchar(40) not null
    constraint django_session_pkey
    primary key,
    session_data text        not null,
    expire_date  timestamp with time zone not null
);

create index if not exists django_session_session_key_c0390e0f_like
on django_session (session_key);

create index if not exists django_session_expire_date_a5c62663
on django_session (expire_date);
