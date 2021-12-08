import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, voltage_sampler
from esphome.const import CONF_ID, CONF_NUMBER
from . import mcp3204_ns, MCP3204

AUTO_LOAD = ["voltage_sampler"]

DEPENDENCIES = ["mcp3204"]

MCP3204Sensor = mcp3204_ns.class_(
    "MCP3204Sensor", sensor.Sensor, cg.PollingComponent, voltage_sampler.VoltageSampler
)
CONF_REFERENCE_VOLTAGE = "reference_voltage"
CONF_MCP3204_ID = "mcp3204_id"

# TODO: figure out how to only allow 4 or 8 channels
CONFIG_SCHEMA = sensor.SENSOR_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(MCP3204Sensor),
        cv.GenerateID(CONF_MCP3204_ID): cv.use_id(MCP3204),
        cv.Required(CONF_NUMBER): cv.int_,
        cv.Optional(CONF_REFERENCE_VOLTAGE, default="3.3V"): cv.voltage,
    }
).extend(cv.polling_component_schema("1s"))


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MCP3204_ID])
    var = cg.new_Pvariable(
        config[CONF_ID],
        parent,
        config[CONF_NUMBER],
        config[CONF_REFERENCE_VOLTAGE],
    )
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
