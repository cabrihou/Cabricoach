-- Coach Cabritos · esquema de sincronización
-- Correr una sola vez en el SQL Editor del proyecto de Supabase (supabase.com → SQL Editor → New query → pegar → Run).
-- Luego en la app: MÁS → NUBE (SUPABASE) → pegar Project URL y anon key (Settings → API).

create table if not exists public.kv (
  house text not null,          -- código de casa compartido entre los dos teléfonos
  uid   text not null,          -- 'andres' | 'cami' | 'shared' (mercado)
  k     text not null,          -- clave del estado (weights, logs, meal, …)
  v     jsonb,
  updated_at timestamptz not null default now(),
  primary key (house, uid, k)
);

alter table public.kv enable row level security;

-- La app usa la anon key sin login; el aislamiento real lo da el código de casa.
-- Cualquiera con la anon key del proyecto podría leer/escribir: no compartas la key
-- y usa un código de casa no obvio.
drop policy if exists "kv acceso anon" on public.kv;
create policy "kv acceso anon" on public.kv
  for all to anon using (true) with check (true);

-- Fotos de registro compartidas (bucket público; la privacidad la da el código de casa en la ruta)
insert into storage.buckets (id, name, public) values ('fotos','fotos', true)
  on conflict (id) do nothing;
drop policy if exists "fotos anon all" on storage.objects;
create policy "fotos anon all" on storage.objects
  for all to anon using (bucket_id = 'fotos') with check (bucket_id = 'fotos');
