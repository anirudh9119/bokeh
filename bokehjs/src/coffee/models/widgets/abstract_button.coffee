_ = require "underscore"

Widget = require "./widget"
p = require "../../core/properties"

class AbstractButton extends Widget.Model
  type: "AbstractButton"

  props: ->
    return _.extend {}, super(), {
      callback: [ p.Instance          ]
      label:    [ p.String, "Button"  ]
      icon:     [ p.String            ]
      type:     [ p.String, "default" ] # TODO (bev)
    }

module.exports =
  Model: AbstractButton