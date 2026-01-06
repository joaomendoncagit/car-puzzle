; benchmark generated from python API
(set-info :status unknown)
(declare-fun r_0_0 () Int)
(declare-fun c_0_0 () Int)
(declare-fun r_1_0 () Int)
(declare-fun c_1_0 () Int)
(assert
 (= r_0_0 0))
(assert
 (= c_0_0 2))
(assert
 (= r_1_0 2))
(assert
 (= c_1_0 0))
(assert
 (let (($x32 (>= r_0_0 0)))
 (and $x32 (< r_0_0 6))))
(assert
 (let (($x39 (>= c_0_0 0)))
 (and $x39 (< c_0_0 6))))
(assert
 (< (- (+ r_0_0 3) 1) 6))
(assert
 (let (($x60 (>= r_1_0 0)))
 (and $x60 (< r_1_0 6))))
(assert
 (let (($x68 (>= c_1_0 0)))
 (and $x68 (< c_1_0 6))))
(assert
 (< (- (+ c_1_0 1) 1) 6))
(assert
 (let ((?x82 (+ c_1_0 0)))
 (let (($x84 (and (distinct c_0_0 ?x82) true)))
 (or (and (distinct (+ r_0_0 0) r_1_0) true) $x84))))
(assert
 (let ((?x82 (+ c_1_0 0)))
 (let (($x84 (and (distinct c_0_0 ?x82) true)))
 (or (and (distinct (+ r_0_0 1) r_1_0) true) $x84))))
(assert
 (let ((?x82 (+ c_1_0 0)))
 (let (($x84 (and (distinct c_0_0 ?x82) true)))
 (or (and (distinct (+ r_0_0 2) r_1_0) true) $x84))))
(assert
 (= r_1_0 2))
(assert
 (= c_1_0 5))
(check-sat)
