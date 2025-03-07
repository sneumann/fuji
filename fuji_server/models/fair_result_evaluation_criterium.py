# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from fuji_server.models.base_model_ import Model
from fuji_server import util


class FAIRResultEvaluationCriterium(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, metric_test_name: str=None, metric_test_score: float=None, metric_test_maturity: int=None, metric_test_status: str='fail'):  # noqa: E501
        """FAIRResultEvaluationCriterium - a model defined in Swagger

        :param metric_test_name: The metric_test_name of this FAIRResultEvaluationCriterium.  # noqa: E501
        :type metric_test_name: str
        :param metric_test_score: The metric_test_score of this FAIRResultEvaluationCriterium.  # noqa: E501
        :type metric_test_score: float
        :param metric_test_maturity: The metric_test_maturity of this FAIRResultEvaluationCriterium.  # noqa: E501
        :type metric_test_maturity: int
        :param metric_test_status: The metric_test_status of this FAIRResultEvaluationCriterium.  # noqa: E501
        :type metric_test_status: str
        """
        self.swagger_types = {
            'metric_test_name': str,
            'metric_test_score': float,
            'metric_test_maturity': int,
            'metric_test_status': str
        }

        self.attribute_map = {
            'metric_test_name': 'metric_test_name',
            'metric_test_score': 'metric_test_score',
            'metric_test_maturity': 'metric_test_maturity',
            'metric_test_status': 'metric_test_status'
        }
        self._metric_test_name = metric_test_name
        self._metric_test_score = metric_test_score
        self._metric_test_maturity = metric_test_maturity
        self._metric_test_status = metric_test_status

    @classmethod
    def from_dict(cls, dikt) -> 'FAIRResultEvaluationCriterium':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FAIRResultEvaluationCriterium of this FAIRResultEvaluationCriterium.  # noqa: E501
        :rtype: FAIRResultEvaluationCriterium
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metric_test_name(self) -> str:
        """Gets the metric_test_name of this FAIRResultEvaluationCriterium.


        :return: The metric_test_name of this FAIRResultEvaluationCriterium.
        :rtype: str
        """
        return self._metric_test_name

    @metric_test_name.setter
    def metric_test_name(self, metric_test_name: str):
        """Sets the metric_test_name of this FAIRResultEvaluationCriterium.


        :param metric_test_name: The metric_test_name of this FAIRResultEvaluationCriterium.
        :type metric_test_name: str
        """

        self._metric_test_name = metric_test_name

    @property
    def metric_test_score(self) -> float:
        """Gets the metric_test_score of this FAIRResultEvaluationCriterium.


        :return: The metric_test_score of this FAIRResultEvaluationCriterium.
        :rtype: float
        """
        return self._metric_test_score

    @metric_test_score.setter
    def metric_test_score(self, metric_test_score: float):
        """Sets the metric_test_score of this FAIRResultEvaluationCriterium.


        :param metric_test_score: The metric_test_score of this FAIRResultEvaluationCriterium.
        :type metric_test_score: float
        """

        self._metric_test_score = metric_test_score

    @property
    def metric_test_maturity(self) -> int:
        """Gets the metric_test_maturity of this FAIRResultEvaluationCriterium.


        :return: The metric_test_maturity of this FAIRResultEvaluationCriterium.
        :rtype: int
        """
        return self._metric_test_maturity

    @metric_test_maturity.setter
    def metric_test_maturity(self, metric_test_maturity: int):
        """Sets the metric_test_maturity of this FAIRResultEvaluationCriterium.


        :param metric_test_maturity: The metric_test_maturity of this FAIRResultEvaluationCriterium.
        :type metric_test_maturity: int
        """

        self._metric_test_maturity = metric_test_maturity

    @property
    def metric_test_status(self) -> str:
        """Gets the metric_test_status of this FAIRResultEvaluationCriterium.


        :return: The metric_test_status of this FAIRResultEvaluationCriterium.
        :rtype: str
        """
        return self._metric_test_status

    @metric_test_status.setter
    def metric_test_status(self, metric_test_status: str):
        """Sets the metric_test_status of this FAIRResultEvaluationCriterium.


        :param metric_test_status: The metric_test_status of this FAIRResultEvaluationCriterium.
        :type metric_test_status: str
        """
        allowed_values = ["pass", "fail"]  # noqa: E501
        if metric_test_status not in allowed_values:
            raise ValueError(
                "Invalid value for `metric_test_status` ({0}), must be one of {1}"
                .format(metric_test_status, allowed_values)
            )

        self._metric_test_status = metric_test_status
