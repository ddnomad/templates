#[macro_export]
macro_rules! impl_bidirectional_string_enum {
    (
        $(
            ($ty:ty, $error_ty:ty, $error_func:expr) {
                $( $variant:ident : $string:literal ),*
            }
        ),*
    ) => {
        $(
            impl std::fmt::Display for $ty {
                fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                    let string = match self {
                        $( Self::$variant => $string, )*
                    };
                    
                    formatter.write_str(string)
                }
            }
            
            impl std::str::FromStr for $ty {
                type Err = $error_ty;
                
                fn from_str(string: &str) -> Result<Self, Self::Err> {
                    match string {
                        $( $string => Ok(Self::$variant), )*
                        other => Err($error_func("invalid value", string))
                    }
                }
            }
        )*
    };
}


#[macro_export]
macro_rules! impl_from_for_enum {
    (
        $(
            $ty:ty {
                $( $variant:ident : $from_type:ty ),*
            }
        ),*
    ) => {
        $(
            $(
                impl From<$from_type> for $ty {
                    fn from(value: $from_type) -> Self {
                        Self::$variant(value.into())
                    }
                }
            )*
        )*
    };
}
