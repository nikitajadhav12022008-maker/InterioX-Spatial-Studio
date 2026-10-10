-- InterioX reference schema (PostgreSQL + PostGIS). SQLAlchemy models create the
-- core tables automatically; use this file for manual setup / spatial extras.
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  mobile TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  scope TEXT CHECK (scope IN ('house','room')) DEFAULT 'house',
  layout JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON projects (owner_id);

CREATE TABLE catalog_items (
  id TEXT PRIMARY KEY, name TEXT, room TEXT, category TEXT, style TEXT DEFAULT 'any',
  price NUMERIC(10,2), width_cm REAL, depth_cm REAL, height_cm REAL,
  lumens INT DEFAULT 0, obstacle BOOLEAN DEFAULT true, glb_url TEXT DEFAULT ''
);

CREATE TABLE designers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL, city TEXT NOT NULL, specialty TEXT,
  rating REAL DEFAULT 0, reviews INT DEFAULT 0,
  location GEOGRAPHY(Point, 4326)          -- PostGIS: "designers near me"
);
CREATE INDEX designers_location_gix ON designers USING GIST (location);

CREATE TABLE review_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  designer_id UUID REFERENCES designers(id),
  project_id UUID,
  contact_name TEXT, contact_phone TEXT, message TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Example: 5 nearest designers to a point (Pune)
-- SELECT name, ST_Distance(location, ST_MakePoint(73.8567,18.5204)::geography)/1000 AS km
-- FROM designers ORDER BY location <-> ST_MakePoint(73.8567,18.5204)::geography LIMIT 5;

-- New in this version
ALTER TABLE projects ADD COLUMN IF NOT EXISTS building_type TEXT DEFAULT 'house';
ALTER TABLE review_requests ADD COLUMN IF NOT EXISTS photo_url TEXT DEFAULT '';

CREATE TABLE ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  value INT CHECK (value BETWEEN 1 AND 5),
  comment TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT now()
);
