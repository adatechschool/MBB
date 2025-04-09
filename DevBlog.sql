CREATE TABLE "User"(
    "id" BIGINT NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "profile_image" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "updated_at" DATE NOT NULL,
    "role_id" BIGINT NOT NULL,
    "follower_id" BIGINT NOT NULL,
    "following_id" BIGINT NOT NULL,
    "bio" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "User" ADD PRIMARY KEY("id");
CREATE TABLE "Post"(
    "post_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "content" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "updated_at" DATE NOT NULL
);
ALTER TABLE
    "Post" ADD PRIMARY KEY("post_id");
CREATE TABLE "Comment"(
    "comment_id" BIGINT NOT NULL,
    "post_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "content" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "updated_at" DATE NOT NULL
);
ALTER TABLE
    "Comment" ADD PRIMARY KEY("comment_id");
CREATE TABLE "Like"(
    "like_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "post_id" BIGINT NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "Like" ADD PRIMARY KEY("like_id");
CREATE TABLE "Follower"(
    "follower_id" BIGINT NOT NULL,
    "created_at" BIGINT NOT NULL
);
ALTER TABLE
    "Follower" ADD PRIMARY KEY("follower_id");
CREATE TABLE "Media"(
    "media_id" BIGINT NOT NULL,
    "post_id" BIGINT NOT NULL,
    "media_url" VARCHAR(255) NOT NULL,
    "media_type" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "updated_at" DATE NOT NULL
);
ALTER TABLE
    "Media" ADD PRIMARY KEY("media_id");
CREATE TABLE "Hashtag"(
    "hashtag_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "created_at" DATE NOT NULL,
    "updated_at" DATE NOT NULL
);
ALTER TABLE
    "Hashtag" ADD PRIMARY KEY("hashtag_id");
CREATE TABLE "PostHashtag"(
    "post_id" BIGINT NOT NULL,
    "hashtag_id" BIGINT NOT NULL
);
ALTER TABLE
    "PostHashtag" ADD PRIMARY KEY("post_id");
CREATE TABLE "Role"(
    "role_id" BIGINT NOT NULL,
    "role_name" VARCHAR(255) CHECK
        ("role_name" IN('')) NOT NULL
);
ALTER TABLE
    "Role" ADD PRIMARY KEY("role_id");
CREATE TABLE "Session"(
    "session_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "token" BIGINT NOT NULL,
    "created_at" DATE NOT NULL,
    "expires_at" DATE NOT NULL
);
ALTER TABLE
    "Session" ADD PRIMARY KEY("session_id");
CREATE TABLE "Following"(
    "following_id" BIGINT NOT NULL,
    "created_at" DATE NOT NULL
);
ALTER TABLE
    "Following" ADD PRIMARY KEY("following_id");
ALTER TABLE
    "Post" ADD CONSTRAINT "post_post_id_foreign" FOREIGN KEY("post_id") REFERENCES "PostHashtag"("post_id");
ALTER TABLE
    "Comment" ADD CONSTRAINT "comment_post_id_foreign" FOREIGN KEY("post_id") REFERENCES "Post"("post_id");
ALTER TABLE
    "Comment" ADD CONSTRAINT "comment_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "User"("id");
ALTER TABLE
    "Media" ADD CONSTRAINT "media_post_id_foreign" FOREIGN KEY("post_id") REFERENCES "Post"("post_id");
ALTER TABLE
    "Session" ADD CONSTRAINT "session_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "User"("id");
ALTER TABLE
    "PostHashtag" ADD CONSTRAINT "posthashtag_hashtag_id_foreign" FOREIGN KEY("hashtag_id") REFERENCES "Hashtag"("hashtag_id");
ALTER TABLE
    "User" ADD CONSTRAINT "user_follower_id_foreign" FOREIGN KEY("follower_id") REFERENCES "Follower"("follower_id");
ALTER TABLE
    "User" ADD CONSTRAINT "user_role_id_foreign" FOREIGN KEY("role_id") REFERENCES "Role"("role_id");
ALTER TABLE
    "Like" ADD CONSTRAINT "like_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "User"("id");
ALTER TABLE
    "Post" ADD CONSTRAINT "post_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "User"("id");
ALTER TABLE
    "Like" ADD CONSTRAINT "like_post_id_foreign" FOREIGN KEY("post_id") REFERENCES "Post"("post_id");
ALTER TABLE
    "User" ADD CONSTRAINT "user_following_id_foreign" FOREIGN KEY("following_id") REFERENCES "Following"("following_id");