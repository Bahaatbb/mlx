# Copyright © 2023 Apple Inc.

import unittest

import mlx.core as mx
import mlx.nn as nn
import mlx_tests
import numpy as np


class TestLosses(mlx_tests.MLXTestCase):
    def test_cross_entropy(self):
        logits = mx.array([[0.0, -float("inf")], [-float("inf"), 0.0]])
        targets = mx.array([0, 1])

        # Test with reduction 'none'
        losses_none = nn.losses.cross_entropy(logits, targets, reduction="none")
        expected_none = mx.array([0.0, 0.0])
        self.assertTrue(mx.array_equal(losses_none, expected_none))

        # Test with reduction 'mean'
        losses_mean = nn.losses.cross_entropy(logits, targets, reduction="mean")
        expected_mean = mx.mean(expected_none)
        self.assertEqual(losses_mean, expected_mean)

        # Test with reduction 'sum'
        losses_sum = nn.losses.cross_entropy(logits, targets, reduction="sum")
        expected_sum = mx.sum(expected_none)
        self.assertEqual(losses_sum, expected_sum)

        # Test cases with weights and no label smoothing
        logits = mx.array([[2.0, -1.0], [-1.0, 2.0]])
        targets = mx.array([0, 1])
        weights = mx.array([1.0, 2.0])

        # Reduction 'none'
        losses_none = nn.losses.cross_entropy(
            logits,
            targets,
            weights=weights,
            reduction="none",
        )
        expected_none = mx.array([0.04858735, 0.0971747])  # Calculated losses
        self.assertTrue(
            np.allclose(losses_none, expected_none, atol=1e-5),
            "Test case failed for cross_entropy loss --reduction='none' --weights=[1.0, 2.0]",
        )

        # Reduction 'mean'
        losses_mean = nn.losses.cross_entropy(
            logits,
            targets,
            weights=weights,
            reduction="mean",
        )
        expected_mean = mx.mean(expected_none)
        self.assertTrue(
            np.allclose(losses_mean, expected_mean, atol=1e-5),
            "Test case failed for cross_entropy loss --reduction='mean' --weights=[1.0, 2.0]",
        )

        # Reduction 'sum'
        losses_sum = nn.losses.cross_entropy(
            logits,
            targets,
            weights=weights,
            reduction="sum",
        )
        expected_sum = mx.sum(expected_none)
        self.assertTrue(
            np.allclose(losses_sum, expected_sum, atol=1e-5),
            "Test case failed for cross_entropy loss --reduction='sum' --weights=[1.0, 2.0]",
        )

        # Test case with equal weights and label smoothing > 0
        logits = mx.array(
            [[0, 0.2, 0.7, 0.1, 0], [0, 0.9, 0.2, 0.2, 1], [1, 0.2, 0.7, 0.9, 1]]
        )
        target = mx.array([2, 1, 0])

        losses_none = nn.losses.cross_entropy(
            logits, target, label_smoothing=0.3, reduction="none"
        )
        expected_none = mx.array([1.29693, 1.38617, 1.48176])
        self.assertTrue(
            mx.allclose(expected_none, losses_none),
            "Test case failed for cross_entropy --label_smoothing=0.3 --reduction='none'",
        )

        expected_mean = mx.mean(expected_none)
        losses_mean = nn.losses.cross_entropy(
            logits, target, label_smoothing=0.3, reduction="mean"
        )
        self.assertTrue(
            mx.allclose(losses_mean, expected_mean),
            "Test case failed for cross_entropy --label_smoothing=0.3 --reduction='mean'",
        )

        expected_sum = mx.sum(expected_none)
        losses_sum = nn.losses.cross_entropy(
            logits, target, label_smoothing=0.3, reduction="sum"
        )
        self.assertTrue(
            mx.allclose(losses_sum, expected_sum),
            "Test case failed for cross_entropy --label_smoothing=0.3 --reduction='sum'",
        )

    def test_l1_loss(self):
        predictions = mx.array([0.5, 0.2, 0.9, 0.0])
        targets = mx.array([0.5, 0.2, 0.9, 0.0])

        # Expected result
        expected_none = mx.array([0, 0, 0, 0]).astype(mx.float32)
        expected_sum = mx.sum(expected_none)
        expected_mean = mx.mean(expected_none)

        losses = nn.losses.l1_loss(predictions, targets, reduction="none")
        self.assertTrue(
            mx.array_equal(losses, expected_none),
            "Test failed for l1_loss --reduction='none'",
        )

        losses = nn.losses.l1_loss(predictions, targets, reduction="sum")
        self.assertTrue(mx.array_equal(losses, expected_sum))

        losses = nn.losses.l1_loss(predictions, targets, reduction="mean")
        self.assertTrue(mx.array_equal(losses, expected_mean))

    def test_mse_loss(self):
        predictions = mx.array([0.5, 0.2, 0.9, 0.0])
        targets = mx.array([0.7, 0.1, 0.8, 0.2])

        expected_none = mx.array([0.04, 0.01, 0.01, 0.04])
        expected_mean = mx.mean(expected_none)
        expected_sum = mx.sum(expected_none)

        # Test with reduction 'none'
        losses_none = nn.losses.mse_loss(predictions, targets, reduction="none")
        self.assertTrue(
            np.allclose(losses_none, expected_none, 1e-5),
            "Test case failed for mse_loss --reduction='none'",
        )

        # Test with reduction 'mean'
        losses_mean = nn.losses.mse_loss(predictions, targets, reduction="mean")
        self.assertEqual(
            losses_mean,
            expected_mean,
            "Test case failed for mse_loss --reduction='mean'",
        )

        # Test with reduction 'sum'
        losses_sum = nn.losses.mse_loss(predictions, targets, reduction="sum")
        self.assertEqual(
            losses_sum, expected_sum, "Test case failed for mse_loss --reduction='sum'"
        )

    def test_smooth_l1_loss(self):
        predictions = mx.array([1.5, 2.5, 0.5, 3.5])
        targets = mx.array([1.0, 2.0, 0.5, 2.5])
        beta = 1.0

        # Expected results
        expected_none = mx.array([0.125, 0.125, 0.0, 0.5])
        expected_sum = mx.sum(expected_none)
        expected_mean = mx.mean(expected_none)

        # Test with reduction 'none'
        loss_none = nn.losses.smooth_l1_loss(
            predictions, targets, beta, reduction="none"
        )
        self.assertTrue(
            mx.array_equal(loss_none, expected_none),
            "Test case failed for smooth_l1_loss --reduction='none'",
        )

        # Test with reduction 'sum'
        loss_sum = nn.losses.smooth_l1_loss(predictions, targets, beta, reduction="sum")
        self.assertEqual(
            loss_sum,
            expected_sum,
            "Test case failed for smooth_l1_loss --reduction='sum'",
        )

        # Test with reduction 'mean'
        loss_mean = nn.losses.smooth_l1_loss(
            predictions, targets, beta, reduction="mean"
        )
        self.assertEqual(
            loss_mean,
            expected_mean,
            "Test case failed for smooth_l1_loss --reduction='mean'",
        )

    def test_nll_loss(self):
        logits = mx.array([[0.0, -float("inf")], [-float("inf"), 0.0]])
        targets = mx.array([0, 1])

        # Test with reduction 'none'
        losses_none = nn.losses.nll_loss(logits, targets, reduction="none")
        expected_none = mx.array([0.0, 0.0])
        self.assertTrue(mx.array_equal(losses_none, expected_none))

        # Test with reduction 'mean'
        losses_mean = nn.losses.nll_loss(logits, targets, reduction="mean")
        expected_mean = mx.mean(expected_none)
        self.assertEqual(losses_mean, expected_mean)

        # Test with reduction 'sum'
        losses_sum = nn.losses.nll_loss(logits, targets, reduction="sum")
        expected_sum = mx.sum(expected_none)
        self.assertEqual(losses_sum, expected_sum)

    def test_kl_div_loss(self):
        p_logits = mx.log(mx.array([[0.5, 0.5], [0.8, 0.2]]))
        q_logits = mx.log(mx.array([[0.5, 0.5], [0.2, 0.8]]))

        # Test with reduction 'none'
        losses_none = nn.losses.kl_div_loss(p_logits, q_logits, reduction="none")
        expected_none = mx.array([0.0, 0.831777])
        self.assertTrue(mx.allclose(losses_none, expected_none))

        # Test with reduction 'mean'
        losses_mean = nn.losses.kl_div_loss(p_logits, q_logits, reduction="mean")
        expected_mean = mx.mean(expected_none)
        self.assertTrue(mx.allclose(losses_mean, expected_mean))

        # Test with reduction 'sum'
        losses_sum = nn.losses.kl_div_loss(p_logits, q_logits, reduction="sum")
        expected_sum = mx.sum(expected_none)
        self.assertTrue(mx.allclose(losses_sum, expected_sum))

    def test_triplet_loss(self):
        anchors = mx.array([[1, 2, 3], [1, 2, 3]])
        positives = mx.array([[4, 5, 6], [0, -1, 2]])
        negatives = mx.array([[7, 8, 9], [3, 2, 3]])

        # Test with reduction 'none'
        losses_none = nn.losses.triplet_loss(
            anchors, positives, negatives, reduction="none"
        )
        expected_none = mx.array([0, 2.31662])
        self.assertTrue(mx.allclose(losses_none, expected_none))

        # Test with reduction 'mean'
        losses_mean = nn.losses.triplet_loss(
            anchors, positives, negatives, reduction="mean"
        )
        expected_mean = mx.mean(expected_none)
        self.assertTrue(mx.allclose(losses_mean, expected_mean))

        # Test with reduction 'sum'
        losses_sum = nn.losses.triplet_loss(
            anchors, positives, negatives, reduction="sum"
        )
        expected_sum = mx.sum(expected_none)
        self.assertTrue(mx.allclose(losses_sum, expected_sum))

    def test_hinge_loss(self):
        inputs = mx.ones((2, 4))
        targets = mx.zeros((2, 4))
        loss = nn.losses.hinge_loss(inputs, targets, reduction="mean")
        self.assertEqual(loss, 1.0)

    def test_huber_loss(self):
        inputs = mx.ones((2, 4))
        targets = mx.zeros((2, 4))
        loss = nn.losses.huber_loss(inputs, targets, reduction="mean")
        self.assertEqual(loss, 0.5)

    def test_log_cosh_loss(self):
        inputs = mx.ones((2, 4))
        targets = mx.zeros((2, 4))
        loss = nn.losses.log_cosh_loss(inputs, targets, reduction="mean")
        self.assertAlmostEqual(loss.item(), 0.433781, places=6)


if __name__ == "__main__":
    unittest.main()
