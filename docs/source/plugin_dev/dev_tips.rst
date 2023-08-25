
Some tips to plugin development
===============================

The following tips are useful to 

Help message
------------

Use :meth:`~mcdreforged.plugin.server_interface.PluginServerInterface.register_help_message` to add some necessary tips for your plugin,
so the player can use ``!!help`` command to know about your plugin

Of course if your plugin is supposed to only be used by player with enough permission level, specify the *permission* argument when registering

Translation
-----------

For :ref:`plugin_dev/plugin_format:Multi file Plugin`, you can also include a ``lang/`` folder in your plugin,
with translation files in json (``.json``) or yaml (``.yml``) format named like ``en_us.json``. MCDR will automatically register these translations for your plugin

It's highly recommended to use your plugin id as the prefix of your translation key, so there will be no translation conflicts between plugins.
e.g. use ``my_plugin.some.text`` instead of ``some.text`` as translation key

The translation key could be expressed as node name which under root node or the path of a nested multi-level nodes.
For example, the following definitions of the translation key ``my_plugin.some.text`` in a language file in yaml (``.yml``) format are equivalent.

.. code-block:: yaml

    my_plugin.some.text: Text of translation key.


.. code-block:: yaml

    my_plugin:
      some:
        text: Text of translation key.


For the difference between 2 translation method in :class:`~mcdreforged.plugin.server_interface.ServerInterface`, let's use Minecraft code (yarn mapping) as an example:

* :meth:`~mcdreforged.plugin.server_interface.ServerInterface.tr` is ``I18n.translate()``
* :meth:`~mcdreforged.plugin.server_interface.ServerInterface.rtr`, or :class:`~mcdreforged.translation.translation_text.RTextMCDRTranslation` is ``new TranslatableText()``

In general, the second method is recommended for translating things in your plugin, since it smartly use the proper language
for the player or the console to send message, and use MCDR's language for general translation things including message logging

Event listening
---------------

If you don't care about info from non-user source, listen to :ref:`event-user-info` event instead of :ref:`event-general-info` event,
which can improve MCDR's performance when the server is spamming with non-user info (e.g. Pasting schematic with Litematica mod) in the console

If you only care about commands from users, instead of listening to :ref:`event-user-info` event,
you can :ref:`register a command tree <page-command>` to MCDR.
It's much more efficient to develop than handling yourself inside :ref:`event-user-info` event

:ref:`plugin_dev/event:MCDR Stop` event allows you to have as many time as you want to save your data.
Be carefully, don't enter an endless loop, MCDR is waiting for you to exit

Multi-threading
---------------

If you want to do some tasks in your plugin that might take some time to finished, such as network querying or massive file operation,
it's recommended to execute your code into a separated thread instead of directly executing them into your event listener function.
Otherwise it might block the pending task execution

For easier use there's a decorator named :func:`@new_thread <mcdreforged.api.decorator.new_thread.new_thread>`
to help you make your function run in another thread asynchronously

User config, data and log files
-------------------------------

If you want to store some user configuration or user data file,
it's recommend to store them inside the ``config`` folder rather than store them inside the plugin folder

The reason is that user might have their plugins be placed in another directory
or even have multiple MCDR instances to load a same plugin collection directory,
by a configuration option named :ref:`configuration:plugin_directories`

If you store your configuration or data inside the plugin folder,
you can't distinguish which MCDR instance the configuration file belongs to.
You can either store them inside the ``config`` folder directly or a inner folder inside the ``config`` folder like ``config/my_plugin/``,
so the user data can be dedicated for the MCDR instance that loads your plugin

:meth:`~mcdreforged.plugin.server_interface.PluginServerInterface.get_data_folder` method is a nice method for lazyman

For logging files, store them inside ``logs/`` folder is a good idea

External packages
-----------------

Some times you plugin needs some external resource files or requires some other ``.py`` codes as libraries. For these,
you need to rather write your plugin in :ref:`plugin_dev/plugin_format:Multi file Plugin` format and insert them in your plugin,
or somehow convert them into a separated plugin and declare the dependency

Misc
----

* The current working directory is the folder where MCDR is in. **DO NOT** change it since that will mess up everything
* For the :class:`~mcdreforged.info_reactor.info.Info` parameter in :ref:`event-general-info` event etc.,
  don't modify it, just use its public methods and read its properties
