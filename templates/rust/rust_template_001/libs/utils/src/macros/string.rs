#[macro_export]
macro_rules! unindent_oneliner_indoc {
    ($literal:literal) => {
        unindent::unindent(indoc::indoc! { $literal }).replace(['\n', '\t'], "")
    };
}
