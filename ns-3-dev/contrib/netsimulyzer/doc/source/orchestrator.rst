Orchestrator
============

The ``Orchestrator`` manages module wide ``netsimulyzer`` features, receives events, and
manages output from the module. All ``netsimulyzer`` models require a reference
to an ``Orchestrator`` to function.

The `Orchestrator` must be constructed **before** the simulation begins.

To construct an `Orchestrator` pass a path to a file to output. Absolute & relative
paths are accepted.

Relative paths (e.g. ``../example.json``) will be relative to the current working directory.

If just a filename is provided (e.g. ``example.json``), then it will be treated as a
path to the current working directory, like so: ``./example.json``.

The output file is in JSON format. For the schema for the output file
see the `schema.json <https://github.com/usnistgov/NetSimulyzer/blob/master/schema.json>`_
for the application. The '.json' extension is not required, but strongly encouraged.

.. code-block:: C++

  auto orchestrator = CreateObject<netsimulyzer::Orchestrator> ("filename.json");

Most ``Orchestrator`` events are based on the simulation's time, so it may be safely placed at
the global scope if desired.

.. code-block:: C++

  using namespace ns3;
  auto orchestrator = CreateObject<netsimulyzer::Orchestrator> ("global.json");

  int
  main ()
  { /* ... */ }


The output file is created when the ``Orchestrator`` is constructed, but is written to
at the **end** of the simulation.


.. _orchestrator-mobility-polling:

Mobility Polling
----------------

If the ``PollMobility`` attribute is true, then the ``Orchestrator`` will poll
all of its child ``NodeConfiguration`` objects for their current location on the interval defined
by ``MobilityPollInterval``.

If the child ``NodeConfiguration`` has ``UsePositionTolerance`` set to true, then,
the aggregated ``Node`` will be checked if its position is within its ``PositionTolerance``,
and if so the ``Orchestrator`` will not write the position change until
it is beyond the ``PositionTolerance`` in the ``NodeConfiguration``.

If ``NodeConfiguration::UsePositionTolerance`` is false, then the ``Orchestrator``
will always write the position when a ``NodeConfiguration`` is polled.


Time Step and Granularity Hinting
---------------------------------

In order to indicate to the application that the simulation should
be run at a given granularity (e.g. should be examined at the microsecond level)
the ``SetTimeStep`` method may be used. The signature for the method follows:

.. cpp:function:: void Orchestrator::SetTimeStep(Time step, Time::Unit granularity)


This method records a ``step``, or how many time units should advance at one time,
and a ``granularity``, or what level to display time units in the application.

Both values are hints to the application, and do take precedence over user
preference, but may still be changed by the user once the simulation is
loaded into the application.

Properties
----------

+------------------------------+--------------------------------+--------------------+------------------------------------------+
| Name                         | Type                           | Default Value      | Description                              |
+==============================+================================+====================+==========================================+
| TimeStep                     | :ref:`optional-value` <int>    |                n/a | Optional hint to the application for     |
| (Deprecated)                 |                                |                    | the number of milliseconds to advance    |
| Use:                         |                                |                    | the simulation by for one step           |
|``Orchestrator::SetTimeStep`` |                                |                    |                                          |
+------------------------------+--------------------------------+--------------------+------------------------------------------+
| MobilityPollInterval         | Time                           | MilliSeconds (100) | How often to poll each child`            |
|                              |                                |                    | ``NodeConfiguration`` for their          |
|                              |                                |                    | current position. Only enabled if        |
|                              |                                |                    | ``PollMobility`` is true                 |
+------------------------------+--------------------------------+--------------------+------------------------------------------+
| PollMobility                 | bool                           |               true | Flag to toggle polling                   |
|                              |                                |                    | for Node positions                       |
+------------------------------+--------------------------------+--------------------+------------------------------------------+
| StartTime                    | Time                           |               n/a  | Optional start of the time window to     |
|                              |                                |                    | capture events in.                       |
|                              |                                |                    | Events outside the window will           |
|                              |                                |                    | be ignored                               |
+------------------------------+--------------------------------+--------------------+------------------------------------------+
| EndTime                      | Time                           |               n/a  | Optional end of the time window to       |
|                              |                                |                    | capture events in.                       |
|                              |                                |                    | Events outside the window will           |
|                              |                                |                    | be ignored                               |
+------------------------------+--------------------------------+--------------------+------------------------------------------+
