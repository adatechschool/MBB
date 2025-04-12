-- micro_blogging.sql
CREATE TABLE
    "User" (
        "user_id" SERIAL NOT NULL,
        "username" VARCHAR(255) NOT NULL,
        "email" VARCHAR(255) NOT NULL,
        "role_id" INTEGER NOT NULL,
        "password" VARCHAR(255) NOT NULL,
        "profile_picture" bytea NULL,
        "bio" TEXT NULL,
        "created_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL DEFAULT now (),
            "updated_at" TIMESTAMP(0)
        WITH
            TIME zone NULL,
            "follower_id" INTEGER NULL,
            "followee_id" INTEGER NULL
    );

ALTER TABLE "User" ADD PRIMARY KEY ("user_id");

ALTER TABLE "User" ADD CONSTRAINT "user_email_unique" UNIQUE ("email");

CREATE TABLE
    "Post" (
        "post_id" SERIAL NOT NULL,
        "user_id" INTEGER NOT NULL,
        "post_content" TEXT NOT NULL,
        "created_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL DEFAULT now (),
            "updated_at" TIMESTAMP(0)
        WITH
            TIME zone NULL
    );

ALTER TABLE "Post" ADD PRIMARY KEY ("post_id");

CREATE TABLE
    "Comment" (
        "comment_id" SERIAL NOT NULL,
        "post_id" INTEGER NOT NULL,
        "user_id" INTEGER NOT NULL,
        "comment_content" TEXT NOT NULL,
        "created_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL DEFAULT now (),
            "updated_at" TIMESTAMP(0)
        WITH
            TIME zone NULL
    );

ALTER TABLE "Comment" ADD PRIMARY KEY ("comment_id");

CREATE TABLE
    "Like" (
        "like_id" SERIAL NOT NULL,
        "post_id" INTEGER NOT NULL,
        "user_id" INTEGER NOT NULL
    );

ALTER TABLE "Like" ADD PRIMARY KEY ("like_id");

CREATE TABLE
    "Post_Hashtag" (
        "post_id" INTEGER NOT NULL,
        "hashtag_id" INTEGER NOT NULL
    );

ALTER TABLE "Post_Hashtag" ADD PRIMARY KEY ("post_id");

ALTER TABLE "Post_Hashtag" ADD PRIMARY KEY ("hashtag_id");

CREATE TABLE
    "Hashtag" (
        "hashtag_id" SERIAL NOT NULL,
        "hashtag_name" VARCHAR(255) NOT NULL
    );

ALTER TABLE "Hashtag" ADD PRIMARY KEY ("hashtag_id");

CREATE TABLE
    "Role" (
        "role_id" SERIAL NOT NULL,
        "role_name" VARCHAR(255) CHECK ("role_name" IN ('user', 'admin', 'moderator')) NOT NULL DEFAULT 'user'
    );

ALTER TABLE "Role" ADD PRIMARY KEY ("role_id");

CREATE TABLE
    "Session" (
        "session_id" SERIAL NOT NULL,
        "user_id" INTEGER NOT NULL,
        "token" VARCHAR(255) NOT NULL,
        "created_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL DEFAULT now (),
            "expires_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL
    );

ALTER TABLE "Session" ADD PRIMARY KEY ("session_id");

CREATE TABLE
    "Follow" (
        "follower_id" INTEGER NOT NULL,
        "followee_id" INTEGER NOT NULL,
        "followed_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL DEFAULT now ()
    );

ALTER TABLE "Follow" ADD PRIMARY KEY ("follower_id");

ALTER TABLE "Follow" ADD PRIMARY KEY ("followee_id");

CREATE TABLE
    "Media" (
        "media_id" SERIAL NOT NULL,
        "post_id" INTEGER NOT NULL,
        "media_type" VARCHAR(255) CHECK ("media_type" IN ('image', 'video')) NULL DEFAULT 'image',
        "media_content" bytea NULL,
        "created_at" TIMESTAMP(0)
        WITH
            TIME zone NOT NULL DEFAULT now (),
            "updated_at" TIMESTAMP(0)
        WITH
            TIME zone NULL
    );

ALTER TABLE "Media" ADD PRIMARY KEY ("media_id");

ALTER TABLE "Media" ADD CONSTRAINT "media_post_id_unique" UNIQUE ("post_id");

ALTER TABLE "Comment" ADD CONSTRAINT "comment_post_id_foreign" FOREIGN KEY ("post_id") REFERENCES "Post" ("post_id");

ALTER TABLE "Media" ADD CONSTRAINT "media_post_id_foreign" FOREIGN KEY ("post_id") REFERENCES "Post" ("post_id");

ALTER TABLE "Post_Hashtag" ADD CONSTRAINT "post_hashtag_post_id_foreign" FOREIGN KEY ("post_id") REFERENCES "Post" ("post_id");

ALTER TABLE "Hashtag" ADD CONSTRAINT "hashtag_hashtag_id_foreign" FOREIGN KEY ("hashtag_id") REFERENCES "Post_Hashtag" ("hashtag_id");

ALTER TABLE "Session" ADD CONSTRAINT "session_user_id_foreign" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id");

ALTER TABLE "Post" ADD CONSTRAINT "post_user_id_foreign" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id");

ALTER TABLE "User" ADD CONSTRAINT "user_role_id_foreign" FOREIGN KEY ("role_id") REFERENCES "Role" ("role_id");

ALTER TABLE "User" ADD CONSTRAINT "user_followee_id_foreign" FOREIGN KEY ("followee_id") REFERENCES "Follow" ("followee_id");

ALTER TABLE "User" ADD CONSTRAINT "user_follower_id_foreign" FOREIGN KEY ("follower_id") REFERENCES "Follow" ("follower_id");

ALTER TABLE "Like" ADD CONSTRAINT "like_post_id_foreign" FOREIGN KEY ("post_id") REFERENCES "Post" ("post_id");

ALTER TABLE "Like" ADD CONSTRAINT "like_user_id_foreign" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id");

ALTER TABLE "Comment" ADD CONSTRAINT "comment_user_id_foreign" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id");