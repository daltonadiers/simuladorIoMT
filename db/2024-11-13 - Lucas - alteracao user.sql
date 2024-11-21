ALTER TABLE public.users RENAME COLUMN id TO seq;

ALTER TABLE public.users ADD email varchar NULL;
ALTER TABLE public.users ADD "password" varchar NULL;
ALTER TABLE public.users ALTER COLUMN email SET NOT NULL;
ALTER TABLE public.users ALTER COLUMN "password" SET NOT NULL;
