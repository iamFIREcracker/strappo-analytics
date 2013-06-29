#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Publisher


class PassengerWithIdGetter(Publisher):
    def perform(self, repository, passenger_id):
        """Get the passenger identified by ``passenger_id``.

        If such passenger exists, a 'passenger_found' message is published
        containing the passenger details;  on the other hand, if no passenger
        exists with the specified ID, a 'passenger_not_found' message will be
        published
        """
        passenger = repository.get(passenger_id)
        if passenger is None:
            self.publish('passenger_not_found', passenger_id)
        else:
            self.publish('passenger_found', passenger)


class ActivePassengersGetter(Publisher):
    def perform(self, repository):
        """Search for all the active passengers around.

        When done, a 'passengers_found' message will be published, followed by
        the list of active passengers.
        """
        self.publish('passengers_found', repository.get_all_active())


class PassengerCreator(Publisher):
    def perform(self, repository, user_id, origin, destination, seats):
        """Creates a new passenger with the specified set of properties.

        On success a 'passenger_created' message will be published toghether
        with the created user.
        """
        passenger = repository.add(user_id, origin, destination, seats)
        self.publish('passenger_created', passenger)


def serialize(passenger):
    if passenger is None:
        return None
    return dict(id=passenger.id, origin=passenger.origin,
                destination=passenger.destination, seats=passenger.seats)


def _serialize(passenger):
    from app.pubsub.users import serialize as serialize_user
    d = serialize(passenger)
    d.update(user=serialize_user(passenger.user))
    return d


class PassengerSerializer(Publisher):
    def perform(self, passenger):
        """Convert the given passenger into a serializable dictionary.

        At the end of the operation the method will emit a
        'passenger_serialized' message containing the serialized object (i.e.
        passenger dictionary).
        """
        self.publish('passenger_serialized', _serialize(passenger))


class MultiplePassengersSerializer(Publisher):
    def perform(self, passengers):
        """Convert a list of passengers into serializable dictionaries.

        At the end of the operation, the method will emit a
        'passengers_serialized' message containing serialized objects.
        """
        self.publish('passengers_serialized',
                     [_serialize(p) for p in passengers])


class PassengerDeactivator(Publisher):
    def perform(self, repository, passenger_id):
        """Hides the passenger identified by ``passenger_id``.

        If no passenger exists identified by ``passenger_id``, then
        a 'passenger_not_found' message is published together with the given
        passenger ID;  on the other hand, a 'passenger_hid' message is published
        with the updated passenger record.
        """
        passenger = repository.deactivate(passenger_id)
        if passenger is None:
            self.publish('passenger_not_found', passenger_id)
        else:
            self.publish('passenger_hid', passenger)


class PassengerDeviceTokenExtractor(Publisher):
    def perform(self, passenger):
        """Extract the device tokens associated with given passenger.

        At the end of the operation a 'device_token_extracted' message will be
        published, together with the extracted device token.
        """
        self.publish('device_token_extracted',
                     passenger.user.device.device_token)
