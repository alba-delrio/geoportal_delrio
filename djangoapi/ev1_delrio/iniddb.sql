CREATE DATABASE ev1_delrio;

create extension postgis;

create schema d;
 
CREATE TABLE d.clientes (id serial PRIMARY KEY, nombre text, direccion text, telefono text, tipo_cliente text,
    barrio text, geom geometry(Point,25830));

CREATE TABLE d.barrios (id serial PRIMARY KEY, nombre text, codigo text, distrito text, numero_clientes integer,
  area double precision, geom geometry(Polygon,25830));

CREATE TABLE d.rutas (id serial PRIMARY KEY, distancia double precision, tiempo integer, estado text,
  barrio_destino text, numero_paradas integer, geom geometry(LineString,25830));
