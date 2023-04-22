# TODO: have the template dynamically generated from the results dictionary
# TODO: Create results dictionary
# inputs = {
#     "diameter": 36,
#     "height": 76,
#     "internal_pressure": 0,
#     "external_pressure": 0,
#     "tank_type": "FRP",
#     "bottom_head": "Flat",
#     "corrosion_barrier": true,
#     "corrosion_barrier_thickness": 0,
#     "corrosion_liner_thickness": 0,
#     "tensile_force": false,
#     "tensile_force_value": 0,
#     "operating_moment": 0,
#     "outdoor": false,
#     "compressive_force": 0,
#     "snow": true,
#     "snow_Ce": 1,
#     "snow_Ct": "1.1",
#     "snow_Is": "1.1",
#     "snow_Pg": "109",
#     "wind": true,
#     "wind_q": "50",
#     "wind_qi": "65",
#     "wind_qh": "47",
#     "wind_G": "0.85",
#     "wind_Cp": "0.7",
#     "wind_GCpi": "0.18",
#     "seismic": true,
#     "seismic_Ss": "1.74",
#     "seismic_S1": "0.6",
#     "seismic_Fv": 1,
#     "seismic_Fa": 1,
#     "seismic_Tl": 1,
#     "storage_type": "Gas",
#     "specific_gravity": 0,
#     "liquid_height": 0,
#     "top_head": "Flat",
#     "live_load": 0,
#     "dead_load": 0,
#     "shell": "Hand Lay-Up",
#     "hoop_tensile_modulus": 0,
#     "hoop_tensile_strength": 0,
#     "axial_tensile_modulus": 0,
#     "axial_tensile_strength": 0,
#     "tank_name": ""
# }
environmental_vars = {
    'snow': {"name": "Snow Pressure",
             "fields": ['Ce', 'Ct', 'Is', 'Pg'],
             },
    'wind': {"name": "Wind Pressure",
             "fields":  ['q', 'qi', 'qh', 'G', 'Cp', 'GCpi'],
             },
    'seismic': {"name": "Seismic:",
                "fields": ['Ss', 'S1', 'Fv', 'Fa', 'Tl'],
                },
}

TEMPLATE = """
<html>

<head>
  <style>
    body {
      font-family: sans-serif;
    }

    h1 {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 10px;
      text-decoration: underline;
    }

    table {
      border-collapse: collapse;
      margin-bottom: 20px;
      width: 100%;
    }

    th, td {
      padding: 8px;
      text-align: left;
      border: 1px solid #ddd;
      width: 50%;
    }

    th {
      background-color: #ddd;
      text-align: left;

    }

    .category {
      font-weight: bold;
      margin-top: 20px;
      text-decoration: underline;
    }
  </style>
</head>

<body>
  <h1>Tank Design Report</h1>
  <table>
    <tr>
      <th>Thickness</th>
      <td>{{ thickness }} in</td>
    </tr>
  </table>
  <div class="category">Features</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Diameter</td>
      <td>{{ diameter }} in</td>
    </tr>
    <tr>
      <td>Height</td>
      <td>{{ height }} in</td>
    </tr>
    <tr>
      <td>Internal Pressure</td>
      <td>{{ internal_pressure }} psi</td>
    </tr>
    <tr>
      <td>External Pressure</td>
      <td>{{ external_pressure }} psi</td>
    </tr>
    <tr>
      <td>Tank Type</td>
      <td>{{ tank_type }}</td>
    </tr>
    <tr>
      <td>Bottom Head Type</td>
      <td>{{ bottom_head }}</td>
    </tr>
    {% if corrosion_barrier %}
    <tr>
      <td>Corrosion Barrier Thickness</td>
      <td>{{ corrosion_barrier_thickness }} in</td>
    </tr>
    {% if tank_type == 'Dual Laminate' %}
    <tr>
      <td>Corrosion Liner Thickness</td>
      <td>{{ corrosion_liner_thickness }} in</td>
    </tr>
    {% endif %}
    {% endif %}
    <tr>
  </table>
  
  <div class="category">Environment</div>
  
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    {% if not outdoor %}
      <tr>
        <td>Operating Indoors</td>
        <td></td>
    {% endif %}
    {% if tensile_force %}
    <tr>
      <td>Tensile Operating Force</td>
      <td>{{ tensile_force_value }} psi</td>
    </tr>
    {% endif %}
    {% if tensile_force or outdoor %}
    <tr>
      <td>Operating Moment</td>
      <td>{{ operating_moment }} lb-ft</td>
    </tr>
    {% endif %}
    {% if outdoor %}
    <tr>
      <td>Compressive Operating Force</td>
      <td>{{ compressive_force }} psi</td>
    </tr>
    <tr>
      <td>Snow Pressure</td>
      <td>{% if snow %}
      <table>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
      <tr>
        <td>Ce</td>
        <td>{{ snow_Ce }}</td>
      </tr>
      <tr>
        <td>Ct</td>
        <td>{{ snow_Ct }}</td>
      </tr>
      <tr>
        <td>Is</td>
        <td>{{ snow_Is }}</td>
      </tr>
      <tr>
        <td>Pg</td>
        <td>{{ snow_Pg }}</td>
      </tr>
      </table>
      {% else %}N\A{% endif %}</td>
    </tr>
    <tr>
      <td>Wind Speed</td>
      <td>{% if wind %}
      <table>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
      <tr>
        <td>q</td>
        <td>{{ wind_q }}</td>
      </tr>
      <tr>
        <td>qi</td>
        <td>{{ wind_qi }}</td>
      </tr>
      <tr>
        <td>qh</td>
        <td>{{ wind_qh }}</td>
      </tr>
      <tr>
        <td>G</td>
        <td>{{ wind_G }}</td>
      </tr>
      <tr>
        <td>Cp</td>
        <td>{{ wind_Cp }}</td>
      </tr>
      <tr>
        <td>GCpi</td>
        <td>{{ wind_GCpi }}</td>
      </tr>
      </table>
      {% else %}N\A{% endif %}</td>
    </tr>
    <tr>
      <td>Seismic</td>
      <td>{% if seismic %}
      <table>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
      <tr>
        <td>Ss</td>
        <td>{{ seismic_Ss }}</td>
      </tr>
      <tr>
        <td>S1</td>
        <td>{{ seismic_S1 }}</td>
      </tr>
      <tr>
        <td>Fv</td>
        <td>{{ seismic_Fv }}</td>
      </tr>
      <tr>
        <td>Fa</td>
        <td>{{ seismic_Fa }}</td>
      </tr>
      <tr>
        <td>Tl</td>
        <td>{{ seismic_Tl }}</td>
      </tr>
      </table>
      {% else %}N\A{% endif %}</td>
    </tr>    
    {% endif %}
  </table>

  <div class="category">Tank Contents</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Tank Type:</td>
      <td>{{ tank_type }}</td>
    </tr>
    <tr>
      <td>Storage Type</td>
      <td>{{ storage_type }}</td>
    </tr>
    {% if storage_type == 'Liquid' %}
    <tr>
      <td>Specific Gravity</td>
      <td>{{ specific_gravity }}</td>
    </tr>
    {% endif %}
  </table>

  <div class="category">Top Head</div>
  <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Type:</td>
      <td>{{ top_head }}</td>
    </tr>
    <tr>
      <td>Live load</td>
      <td>{{ live_load }} lbf</td>
    </tr>
    <tr>
      <td>Dead load</td>
      <td>{{ dead_load }} lbf</td>
    </tr>
  </table>
   <div class="category">Top Head</div>
   <table>
    <tr>
      <th>Parameter</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Type:</td>
      <td>{{ shell }}</td>
    </tr>
    <tr>
      <td>Hoop Tensile Modulus:</td>
      <td>{{ hoop_tensile_modulus }} psi</td>
    </tr>
    <tr>
      <td>Hoop Tensile Strength</td>
      <td>{{ hoop_tensile_strength }} psi</td>
    </tr>
    <tr>
      <td>Axial Tensile Modulus</td>
      <td>{{ axial_tensile_modulus }} psi</td>
    </tr>
    <tr>
      <td>Axial Tensile Strength</td>
      <td>{{ axial_tensile_strength }} psi</td>
    </tr>
  </table>

</body>

</html>
"""
