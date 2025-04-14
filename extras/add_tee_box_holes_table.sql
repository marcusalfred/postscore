-- Add tee_box_holes table
CREATE TABLE IF NOT EXISTS public.tee_box_holes (
    id TEXT PRIMARY KEY,
    tee_box_id TEXT NOT NULL,
    hole_number integer,
    par integer,
    yardage integer,
    handicap integer,
    created_on timestamp without time zone DEFAULT NOW() NOT NULL
);

ALTER TABLE public.tee_box_holes OWNER TO golf_api;

-- Add foreign key constraints
ALTER TABLE ONLY public.tee_box_holes
    ADD CONSTRAINT tee_box_holes_tee_box_id_fkey FOREIGN KEY (tee_box_id) REFERENCES public.tee_boxes(id);

-- Add foreign key constraint to round_holes
ALTER TABLE ONLY public.round_holes
    ADD CONSTRAINT round_holes_tee_box_hole_id_fkey FOREIGN KEY (tee_box_hole_id) REFERENCES public.tee_box_holes(id); 