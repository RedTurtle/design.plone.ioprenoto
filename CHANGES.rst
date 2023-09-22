Changelog
=========

1.1.6 (2023-09-22)
------------------

- Fix @bookings overrides
  [mamico]

1.1.5 (2023-09-05)
------------------

- Move redirect for anonymous in the frontend
  [mamico]


1.1.4 (2023-08-31)
------------------

- Fixed the manager message stringinterp adapter.
  [folix-01]


1.1.3 (2023-08-11)
------------------

- Fix bad stringinterp adapter definition.
  [folix-01]
- Remove "description" field to customizable PrenotazioniFolder fields.
  [cekk]
- Customize @booking-schema endpoint to set *description* as always required.
  [cekk]
- Url operator
  [mamico]

1.1.2 (2023-07-25)
------------------

- Fix redireect url for anonymous
  [mamico]

- Changed label 'uffici correalti'
  [mamico]

1.1.1 (2023-07-07)
------------------

- fix booking_url in @bookings
  [mamico]

1.1.0 (2023-06-30)
------------------

- Move message to contentrule in iocittadino
  [mamico]

- Handle custom frontend_domain in notification urls (to fix the /admin problem).
  [cekk]

- Fix permission management in PrenotazioniFolder serializer.
  [cekk]

1.0.10 (2023-06-20)
-------------------

- Fix the prentazione created message.
  [folix-01]


1.0.9 (2023-06-19)
------------------

- Fix the prentazione link in the message.
  [folix-01]


1.0.8 (2023-06-19)
------------------

- Edit prenotazione creation message.
  [folix-01]


1.0.7 (2023-06-16)
------------------

- Add title to message created on prenotazione creation(#42314).
  [folix-01]

1.0.6 (2023-06-16)
------------------

- On message creation use `sent` state.
  [folix-01]


1.0.5 (2023-06-16)
------------------

- Add message on Prenotazione creation (#42314).
  [folix-01]


1.0.4 (2023-06-14)
------------------

- Overrides @bookings for booking urls
  [mamico]


1.0.3 (2023-06-13)
------------------

- typo "corellati" vs. "correlati" (+ i18n)
  [mamico]


1.0.2 (2023-06-12)
------------------

- Fix uo-bookable-list esporta solo le stanze pubbliche
  [mamico]

- Customize some stringinterp adapters to use io-comune frontend view.
  [cekk]

1.0.1 (2023-04-06)
------------------

- Fix CI struments configs.
  [foxtrot-dfm1]


1.0.0 (2023-04-06)
------------------

- Initial release.
  [RedTurtle]
