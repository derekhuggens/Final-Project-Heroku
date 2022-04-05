{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled",
      "provenance": [],
      "authorship_tag": "ABX9TyMD5TA53jzSOG8vAfOKnYHv",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/ShazarHub/Final-Project-/blob/postgresql_database_branch/SQL_insurance_fraud_db.sql\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 131
        },
        "id": "MHQDVBEKRZkB",
        "outputId": "38bb7ed1-7635-4e77-b6ec-6743033d912d"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "SyntaxError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-1-db8f870019ff>\"\u001b[0;36m, line \u001b[0;32m1\u001b[0m\n\u001b[0;31m    CREATE TABLE insurance_claims (\u001b[0m\n\u001b[0m               ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
          ]
        }
      ],
      "source": [
        "CREATE TABLE insurance_claims (\n",
        "\tmonths_as_customer INTEGER,\n",
        "\tage INTEGER,\n",
        "\tpolicy_number INTEGER,\n",
        "\tpolicy_bind_date DATE,\n",
        "\tpolicy_state VARCHAR(2),\n",
        "\tpolicy_csl VARCHAR(10),\n",
        "\tpolicy_deductable INTEGER,\n",
        "\tpolicy_annual_premium DECIMAL,\n",
        "\tumbrella_limit INTEGER,\n",
        "\tinsured_zip INTEGER,\n",
        "\tinsured_sex VARCHAR(6),\n",
        "\tinsured_education_level VARCHAR(15),\n",
        "\tinsured_occupation VARCHAR(25),\n",
        "\tinsured_hobbies VARCHAR(15),\n",
        "\tinsured_relationship VARCHAR(15),\n",
        "\tcapital_gains INTEGER,\n",
        "\tcapital_loss INTEGER,\n",
        "\tincident_date DATE,\n",
        "\tincident_type VARCHAR(25),\n",
        "\tcollision_type VARCHAR(20),\n",
        "\tincident_severity VARCHAR(20),\n",
        "\tauthorities_contacted VARCHAR(10),\n",
        "\tincident_state VARCHAR(2),\n",
        "\tincident_city VARCHAR(15),\n",
        "\tincident_location VARCHAR(25),\n",
        "\tincident_hour_of_the_day INTEGER,\n",
        "\tnumber_of_vehicles_involved INTEGER,\n",
        "\tproperty_damage VARCHAR(3),\n",
        "\tbodily_injuries INTEGER,\n",
        "\twitnesses INTEGER,\n",
        "\tpolice_report_available VARCHAR(3),\n",
        "\ttotal_claim_amount INTEGER,\n",
        "\tinjury_claim INTEGER,\n",
        "\tproperty_claim INTEGER,\n",
        "\tvehicle_claim INTEGER,\n",
        "\tauto_make VARCHAR(10),\n",
        "\tautauto_model VARCHAR(15),\n",
        "\tauto_year INTEGER,\n",
        "\tfraud_reported VARCHAR(1),\n",
        "\tPRIMARY KEY (policy_number)\n",
        ");"
      ]
    }
  ]
}