Changelog
=========

1.2.11 (unreleased)
-------------------

- Nothing changed yet.


1.2.10 (2025-03-05)
-------------------

- fix typo
- onceonly con iocittadino
  [mamico]


1.2.9 (2025-01-22)
------------------

- Remove customized rolemap and use default redturtle.prenotazioni rolemap. Booking manager should manage bookings without Editor role.
  [cekk]


1.2.8 (2024-10-17)
------------------

- Fix get prenotazione, for missing gate
  [mamico]


1.2.7 (2024-10-17)
------------------

- Fix add prenotazione, for missing gate
  [mamico]


1.2.6 (2024-08-21)
------------------

- Added more information in the `/@booking/<bookingid>` service (e.g. booking_folder, booking_address, booking_office),
  already present in the `/@bookings?fullobjects=1` service. https://github.com/RedTurtle/design.plone.ioprenoto/pull/41
  These changes will be moved in the future from here to redturtle.prenotazioni 2.3.x
  [mamico]


1.2.5 (2024-04-22)
------------------

- Refactor rest service to simplify inheritance
  [lucabel]
- Add redturtle.prenotazioni's notify_upcoming_bookings script to console_scripts (allows it to be available in the buildout).
  [folix-01]

1.2.4 (2024-04-11)
------------------

- default b_size for booking types vocabulary serializer to 200
  [mamico]


1.2.3 (2024-03-13)
------------------

- Fix problem with DefaultJSONSummarySerializer hineritance in prenotazioniFolder
  DefaultJSONSummarySerializer override.
  [lucabel]
- Add the plone.restapi>=9.6.0 constaint.
  [folix-01]


1.2.2 (2024-01-25)
------------------

- Fix: term values must be unique in booking_type vocabulary
  [mamico]

- Fix booking_type encoding
  [mamico]

1.2.1 (2023-12-19)
------------------

- booking_type vocabulary for Service
  [mamico]
- Align tests with redturtle.prenotazioni > 2.2.5.
  [cekk]


1.2.0 (2023-11-20)
------------------

- [BREAKING CHANGE] Compatibility with redturtle.prenotazioni>=2.2.0.
  [folix-01]
- Handle missing infos in prenotazioniFolder serializer.
  [cekk]
- Add the UO.contact_info field to @bookable-uo-list response.
  [folix-01]
- Extend prenotazioni email vars list (unita_organizzativa_title, booking_print_url_with_delete_token).
  [folix-01]


1.1.10 (2023-10-16)
-------------------

- Inherit redturtle.prenotazioni browser layer.
  [folix-01]


1.1.9 (2023-10-13)
------------------

- Compatibilize with the 2.1.3redturtle.prenotazioni version.
  [folix-01]


1.1.8 (2023-10-13)
------------------

- Update redturtle.prenotazioni version to >= 2.1.1
  [folix-01]
- Add the UO.contact_info field to @bookable-uo-list response.
  [folix-01]


1.1.7 (2023-09-25)
------------------

- Workaround booking_url in @bookings differente per gestori e cittadini
  [mamico]


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
